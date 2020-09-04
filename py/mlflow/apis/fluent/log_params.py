#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_params
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    params = {"learning_rate": 0.01, "n_estimators": 10}

    with mlflow.start_run():
        mlflow.log_params(params)
