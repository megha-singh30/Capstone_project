15-01-2026
- Created a folder structure in the project folder. For this I created a template.py python file to create the desired folder automatically.
- Downloaded the churn prediction file from Kaggle website into data folder.
- Trying to install libraries but new environment.
- Not able to create new environment with Conda.
- Tyring with python way

16-01-2026
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

17-06-2026
- How to activate the environment
   .\capsproj\Scripts\Activate.ps1
   write this directly in powershell
- Learnt about Linting(ruff), type hints and pytest
- Installed ruff and pytest
- run ruff 
> ruff check src\
- Created test_data.py file for pytest to run and check correctness of codes
   - Added functions to test each of 3 functions in data.py, these functions check the output length, type etc to make sure the output returned by those functions are correct.
- Tested with 
> pytest -v
this pointed out with errors, which I corrected, and now says "All tests passed"