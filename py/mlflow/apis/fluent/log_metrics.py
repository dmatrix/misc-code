#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metrics
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    metrics = {"mse": 2500.00, "rmse": 50.00}

    # Log a batch of metrics
    with mlflow.start_run():
        mlflow.log_metrics(metrics)
