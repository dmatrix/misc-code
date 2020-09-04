#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metric
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    with mlflow.start_run():
        mlflow.log_metric("mse", 2500.00)
