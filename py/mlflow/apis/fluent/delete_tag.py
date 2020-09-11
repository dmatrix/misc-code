#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.delete_tag
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    tags = {"engineering": "ML Platform",
            "engineering_remote": "ML Platform"}

    with mlflow.start_run() as run:
        mlflow.set_tags(tags)

    with mlflow.start_run(run_id=run.info.run_id):
        mlflow.delete_tag("engineering_remote")



