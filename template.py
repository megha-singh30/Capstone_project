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
    f"data/"
    f"tests/"
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/data.py",
    f"src/{project_name}/predict.py",
    f"src/{project_name}/train.py",
    f"src/{project_name}/data_ingestion.py",
    "config/config.yaml",
    "requirements.txt", # keeping the list of all packages
    "research/churn_analysis.ipynb", # for experiments done with the data before production release 
    "templates/index.html" # for creating the web application
    "pyproject.toml" # for packaging the project
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