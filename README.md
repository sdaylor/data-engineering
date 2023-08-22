# data-engineering
This repository deploys [Poetry](https://python-poetry.org/) for package management. Once installed,
the virtual environment can be created with the relevant dependencies via `poetry install`. Execute `poetry shell`
to activate the virtual environment.

## Section 1: Consulting Soft Skills
Please refer to the markdown file [soft_skills.md](soft_skills/soft_skills.md).

## Section 2: Database & Python ETL
The relevant files for this section are located in the [db_python_etl](db_python_etl/) directory.
I elected to use the Pandas library over PySpark due to its first class Excel support,
and over [Dask](https://www.dask.org/) or [Pandas on PySpark](https://spark.apache.org/docs/latest/api/python/user_guide/pandas_on_spark/index.html)
since there were only 1,000 records so parallelization would not have a marked benefit.

The ETL script executes the following steps:
1. Connects to the MySQL database [created on Azure by Terraform](db_python_etl/terraform/main.tf)
2. Ingests the Excel file, which I included in the repository for simplicity's sake
3. Creates a new boolean column, `is_public_ip`, via an anonymous function which determines if the user's `ip_address` is publicly allocated
4. Concatenates the `first_name` and `last_name` columns to create a new column `full_name`
5. Apply a MD5 hash function to the user's `email` to create a new column `obfuscated_email`
6. Drop the `first_name`, `last_name`, and `email` columns
7. Write the resulting DataFrame to the `data_engineering` table in the default schema, overwriting if it already exists
8. Dispose of engine's connection pool

I have also included a small [test suite](db_python_etl/tests/test_etl.py) using Pytest. With more time, one should
add additional tests and automate test execution and coverage reports via pre-commit hooks and CI processes.

To reproduce the ETL process:
1. Create an Azure subscription
2. Create an App Registration in Azure AD, generate credentials, and assign it the Contributor IAM role
   to the subscription in Step 1
3. Create a Terraform Cloud workspace and a TF Cloud API token
4. Create an `.env` file using `.env.example` as a template, and fill out the TF-related variables
5. `cd db_python_etl/terraform/` and initialize with `dotenv -f <path-to-env-file> run terraform init`
6. Execute Terraform plan with `dotenv -f <path-to-env-file> run terraform plan`
7. Glean the MySQL connection details from the Terraform state and populate the remaining environment variables in
   your new `.env` file
8. `cd` to `db_python_etl` and execute `dotenv -f <path-to-env-file> run python etl.py`

## Section 3: ML API
The relevant files for this section are located in the [ml_api](ml_api/) directory. I use a simple Flask application
to serve a pre-trained [image classification model](https://imageai.readthedocs.io/en/latest/prediction/index.html)
from ImageAI over an API endpoint. This tooling should not be deployed to a production environment since it uses
Flask's development web server and does not have artifact management, authentication, monitoring, robust error handling,
tests, scaling, et cetera.

To reproduce:
1. Execute `cd ml_api/docker` and `docker build --tag ml-api -f ml_api/docker/Dockerfile .`
2. Execute `docker run -p 5000:5000 ml-api`
3. Alternatively, Flask can be invoked directly within the `ml_api` directory via `flask run` 
4. The API endpoint expects a POST request with two parameters, `image_url` and `prediction_count`:
```curl
curl --location 'http://127.0.0.1:5000/' \
--header 'Content-Type: application/json' \
--data '{
    "image_url": "https://www.atlasandboots.com/wp-content/uploads/2019/05/ama-dablam2-most-beautiful-mountains-in-the-world.jpg",
    "prediction_count": 10
}'
```
