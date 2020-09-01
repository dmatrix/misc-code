#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_params
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    params = {"learning_rate": 0.01, "n_estimators": 10}

    # Creates a run if one is not active and log two parameters
    mlflow.log_params(params)

    # end the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.log_params(params)
