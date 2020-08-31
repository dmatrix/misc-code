#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_params
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    params = {"condition": "Air Quality", "index": 5.0}

    # Create a run if one is not active and log two parameters
    mlflow.start_run()
    mlflow.log_params(params)
    mlflow.end_run()

    # Or you Context Manager create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.log_params(params)
