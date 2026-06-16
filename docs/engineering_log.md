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