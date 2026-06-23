## 15-01-2026 -- DAY-1
- Created a folder structure in the project folder. For this I created a template.py python file to create the desired folder automatically.
- Downloaded the churn prediction file from Kaggle website into data folder.
- Trying to install libraries but new environment.
- Not able to create new environment with Conda.
- Trying with python way

## 16-01-2026 -- DAY-2
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

## 17-06-2026 -- DAY-3
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


## 18-06-2026 -- DAY-4
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

## 19-06-2026 -- DAY-5
> Understanding -- why APIs serve models, not scripts
Scripts: Local execution. Manual setup. Resource intensive. Exposed code
APIs: Cloud execution. Automated access. Managed resources. Protected code
Scripts remain in codes, have to be executed and machine dependent.

- APIs decouples ML logic from front-end app, 
- python can interact with Java or other, 
- IP protection
- scalability, 
- standaradization - inputs are uniform, output can be JSON
- seamless version control

> [ User Request ] -> [ Web/Mobile App ] -> [ API Endpoint ] -> [ Model Predicts ] -> [ JSON Response ]

Python-based frameworks:
1. Django
2. FastAPI -- automatic input validation with Pydantic model types, has auto-generated documentation, direct Dict returns
3. Flask

in the APi code, added customer model with all features datatype, then added predict function, which takes the input from the service, preprocess it using preprocessing done inside, the using reindex to make features in same order as training and filling them 0 if not provided and then running the model probability calculation with this processed code.

a service stays alive and answers prediction requests on demand (your API). 

## 22-06-2026 -- DAY-6
Learning how to dockerize the API.
"Dockerizing an API" means packaging an Application Programming Interface (API) alongside its source code, runtime, system tools, and dependencies into a single, isolated unit called a container image

- The Dockerfile: A text file placed in the root of your API project containing a step-by-step blueprint of commands to assemble the container image
- The Dockerfile: A text file placed in the root of your API project containing a step-by-step blueprint of commands to assemble the container image
- The Container: The active, living instance of your image running as an isolated process on a host machine.
- Eliminates "It Works on My Machine": Your API carries its exact framework and system version, neutralizing configuration conflicts. Can be run on any machine

- Docker Compose is a tool used for defining and running multi-container Docker applications
Instead of typing long, complex terminal commands to launch and connect your API, database, and caching systems one by one, you define your entire infrastructure in a single text file named docker-compose.yml. You can then launch your entire stack with one command: docker compose up

- Every container has its own isolated localhost that points to itself. So if your API tried to reach the database at localhost:5432, it'd look for Postgres inside the API container — where nothing's running — and fail. The database is in a different container.
Compose solves this by putting both containers on a shared private network where each container is reachable by its service name. Your compose file names the database service db, so from inside the API container, the hostname db resolves to the Postgres container. That's why the connection string is @db:5432 — db is the address of the other container on that network.
One-line version to lock in: localhost inside a container = that container itself; to reach a different container, you use its service name, which compose's network resolves for you.
________________________________________
Created dockerfile.api and docker-compose.yaml file 
docker compose up --build
http://localhost:8000/health
http://localhost:8000/docs
docker compose ps
docker compose down

# Review Week-1
- Notebook code → installable src/churn_predictor package. Fought ModuleNotFoundError, editable installs, the python -m quirk, a Windows \t path bug.
- ruff + pytest; 3 real tests that caught actual bugs (path resolution, features-vs-train/test confusion).
- Docker fundamentals — image vs container, layers, lifecycle. Install + hello-world.
- Dockerized training; empty-requirements trap, transitive deps, CMD exec-form, volume mount to persist the model artifact.
- FastAPI /health + /predict; solved training/serving skew via reindex to feature_names_in_. Verified with contrasting profiles (0.03 vs 0.4).
- Multi-container compose stack (API + Postgres); service-name networking (db not localhost), 0.0.0.0 host binding.