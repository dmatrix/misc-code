#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metrics
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    metrics = {"mse": 2500.00, "rsme": 50.00}

    # Create a run if one is not active and log two metrics
    mlflow.start_run()
    mlflow.log_metrics(metrics)
    mlflow.end_run()

    # Or you Context Manager create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.log_metrics(metrics)
