# This template helps to generate a general folder structure automatically 
# to begin any ML project

# There are various steps in the project
# Those steps are listed below; along with their corresponding code lines

import os
from pathlib import Path
import logging

## 1. Basic Logging Initialization #############################################

project_name = "churn_predictor"

logging.basicConfig(level=logging.INFO,
                    format = "%(asctime)s | %(filename)s | %(message)s")

## 2. List of folders to be created ############################################

list_of_files = [
    ".github/workflows/.gitkeep", # this is used to keep the files for CI/CD pipelines (deployment)
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml", # for model deployment, to track pipelines and data versioning
    "params.yaml",
    "requirements.txt", # keeping the list of all packages to be used by setup.py
    "setup.py",
    "research/churn_analysis.ipynb", # for experiments done with the data before production release 
    "templates/index.html" # for creating the web application
]

#3 3. Convert the list into actual path to create folders ############################

for filepath in list_of_files:
        filepath = Path(filepath) # helps to convert forward slash strings to Windows path

        filedir, filename = os.path.split(filepath)

        if filedir!="":
                os.makedirs(filedir, exist_ok=True)
                logging.info(f"Creating directory: {filedir} for the file : {filename}")

        if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
                with open(filepath, "w") as f:
                        pass
                        logging.info(f"Creating empty file: {filepath}")
        else:
                logging.info(f"{filename} already exists")