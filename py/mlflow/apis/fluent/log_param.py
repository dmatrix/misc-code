#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_param
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    with mlflow.start_run():
        mlflow.log_param("learning_rate", 0.01)



