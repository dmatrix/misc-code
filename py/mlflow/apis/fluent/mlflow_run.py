#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow_run
#
import warnings
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    project_uri = "https://github.com/mlflow/mlflow-example"
    params = {"alpha": 0.5, "l1_ratio": 0.01}

    # Run MLflow project and create a reproducible conda environment
    # on local host
    mlflow.run(project_uri, parameters=params)

