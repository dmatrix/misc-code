#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metric
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    metrics = {"mse": 2500.00, "rmse": 50.00}

    # Creates a run if one is not active and log metrics
    [mlflow.log_metric(key, value) for key, value in metrics.items()]

    # end the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run and log metrics
    with mlflow.start_run(run_name="My Runs"):
        [mlflow.log_metric(key, value) for key, value in metrics.items()]
