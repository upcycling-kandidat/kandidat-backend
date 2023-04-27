# kandidat-backend
## Prerequisite
Below you will find the prerequisites for running the project locally.
### Create a .env file
Begin with creating an environment variable file called `.env` in the root of the project. This file will contain the credentials for e.g. MinIO object storage. The file should look like this:
```bash
cp .env-example .env
```

### Setup conda
You will need to have conda installed on the system. Miniconda should suffice
[install miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Clone the repo
```bash
git clone git@github.com:upcycling-kandidat/kandidat-backend.git
cd kandidat-backend
```
### Create a new conda environment
```bash
conda env create --file environment.yml
``` 
This will look for the environment.yml file and create a new environment called chair-training. To activate this new environment, run the following command:
```bash
conda activate kandidat-backend
```

**Further information about conda environments can be found [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)**

## Host MinIO object storage
You will need to have docker installed on the system. [install docker](https://docs.docker.com/get-docker/)
Run the following command to start the MinIO object storage container
```bash	
docker compose up -d
```

## The code 
When accessing environment variables alway use `python-dotenv` package. This will make sure that the environment variables are loaded from the `.env` file. Make sure to follow [Create a .env file](#create-a-.env-file) before running the code.

Example showing how to access the environment variable `MINIO_ACCESS_KEY`:
```python
from dotenv import dotenv_values

config = dotenv_values(".env")
config["MINIO_ACCESS_KEY"]
```

In `storage.py` you will find the `upload_file` function which takes in one argument `input_file` which is a path of the desired file to upload.

To add a new endpoint, create a new function in `app.py` and add the endpoint to the `app` object. Example showing how to add a new endpoint which accepts HTTP `POST` methods with the path `/test` which returns a json object:
```python
from flask import (
    jsonify,
    request,
)

@app.route("/test", methods=["POST"])
# The function name can be anything
def test():
    if request.method == "POST":
        return jsonify({"message": "test"})
  return
```

## Tech stack
The project uses `Flask` as the web framework to serve the REST API and `MinIO` as the object storage. The project is written in `Python 3.8.5`.