## 15-01-2026
- Created a folder structure in the project folder. For this I created a template.py python file to create the desired folder automatically.
- Downloaded the churn prediction file from Kaggle website into data folder.
- Trying to install libraries but new environment.
- Not able to create new environment with Conda.
- Trying with python way

## 16-01-2026
- Learnt about - 
 - why notebooks don't ship
    Good for prototyping, exploration and visualization. Notebooks are not a structured code, generally disorganized, no order. Also has hidden states, when run out of order. Variables do not get deleted, but misinterpreted in various cells under multiple uses. No versioning, no debugging, but lot of large data, dataframes, figures, metadata 
 - why a train() function beats a training cell in a notebook?
    So that is a reason, we dont want notebooks in production but independent structure based functions, like train(), to ensure correctness and reprodicibility.

    ## Production-grade project structure ensures high code quality which means correctness and reproducibility

    ## Day 1 — repo + modularization
- Built: src/ package, moved notebook → data/train/predict, model trains (AUC 0.842)
- Broke: ModuleNotFoundError on churn_predictor
- Root cause: package buried in src/, not on path; editable install's default mode
  doesn't support `python -m`; Windows `\t` path-escape ate my CSV path
- Fixed: pyproject + `pip install -e . --config-settings editable_mode=compat`; pathlib paths
- Learned: how Python actually resolves packages
- In short, downloaded the data, made a new environment, then run 
> pip install -e ".[dev]"
- created major .py files -> data -> train -> predict
- Finally running -
> python -m churn_predictor.train

Tried these commands in order:
> pip install -e .
> python -c "import sys; print(sys.executable)"
> pip -V
> python -m pip install -e .
> python -c "import churn_predictor; print(churn_predictor.__file__)"
> python -c "from churn_predictor import data; print(data.__file__)"
> python -m pip install -e . --config-settings editable_mode=compat

## 17-06-2026
- How to activate the environment
> .\capsproj\Scripts\Activate.ps1  
> pip show churn_predictor
   write this directly in powershell
- Learnt about Linting(ruff), type hints and pytest
- Installed ruff and pytest
> pip install pytest ruff  
- run ruff 
> ruff check src\
- Created test_data.py file for pytest to run and check correctness of codes
   - Added functions to test each of 3 functions in data.py, these functions check the output length, type etc to make sure the output returned by those functions are correct.
- Tested with 
> pytest -v
this pointed out with errors, which I corrected, and now says "All tests passed"
Below is the output
'''bash
=========== test session starts ===================================
platform win32 -- Python 3.11.5, pytest-9.1.0, pluggy-1.6.0 -- C:\Users\Megha Singh\Documents\Python\Projects\Capstone_project\.capsproj\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Megha Singh\Documents\Python\Projects\Capstone_project
configfile: pyproject.toml
collected 3 items                                                                                                    

tests/test_data.py::test_load_returns_dataframe_with_churn PASSED                                              [ 33%]
tests/test_data.py::test_preprocess_makes_totalcharges_numeric PASSED                                          [ 66%]
tests/test_data.py::test_split_rows_add_up PASSED                                                              [100%]

=============== 3 passed in 0.43s ======================================
'''

>  python -m churn_predictor.train  

- I also finished learning how to run docker
List of commands I followed after installing Docker Desktop
- code -install-extension ms-vscode-remote.remote-wsl
- docker --version 
- docker run hello-world 
> Here created one python file named hello.py, and one Dockerfile with 3 statements to run hello.py file
- docker build -t hello-mlops .   --> builds an image
- docker run hello-mlops -> container runs the image
docker ps -a          # all containers (running + stopped)
docker images         # images you've built
docker logs <id>      # what a container printed
docker rm <id>        # delete a stopped container
docker rmi hello-mlops  # delete the image
docker rm <hello-mlops-id>    # remove the stopped container
docker rm sleeper             # and the sleeper
docker rmi hello-mlops        # remove the image
docker images                 # confirm it's gone


## 18-06-2026
> Version Pinning
practice to freeze software project dependencies (libraries, plugins or tools) to exact number versions
it helps - 
- to work on any machine
- no automatic update
- ensures reproducibility
- example - 
      - Unpinned - pandas >= 2.2.0
      - Pinned -   pandas == 2.2.2
- valid for Docker also -
      - Unpinned - image: python:3.11
      - Pinned -   image: python: 3.11.7

> Slim Base Images
stripped down versions of standard container OS(Debian/Ubuntu)

> pip freeze
- This helped me to pin libraries in requirements.txt --> only those libraries that project files required
- Added those files to requirements.txt

> Dockerisation
> docker build -t churn-trainer . 
> docker run -v ${PWD}/models:/app/models churn-trainer 

docker run itself does not make the joblib file. It does one thing: start a container from your image and execute its CMD — which is python -m churn_predictor.train. So docker run runs your training script.
Then train.py (running inside the container) is what creates the file — its joblib.dump(model, "models/model.joblib") line writes the artifact to /app/models/model.joblib inside the container.
The -v ${PWD}/models:/app/models part is the piece that makes it appear on your machine. Think of it as a shared window between two rooms:

your host's models/ folder (your room)
the container's /app/models/ folder (its room)

