#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.delete_tag
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    tags = {"engineering": "ML Platform",
            "engineering_remote": "ML Platform",
            "release.candidate": "RC1",
            "release.version": "2.2.0"}

    with mlflow.start_run():
        for key, value in tags.items():
            mlflow.set_tag(key, value)
        mlflow.delete_tag("engineering_remote")



