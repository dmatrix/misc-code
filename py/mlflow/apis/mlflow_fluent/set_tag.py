#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.set_tag
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Creates a run if one is not active and set three tags
    mlflow.set_tag("engineering", "ML")
    mlflow.set_tag("release.candidate", "RC1")
    mlflow.set_tag("release.version", "2.2.0")

    # end the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.set_tag("engineering", "ML")
        mlflow.set_tag("release.candidate", "RC1")
        mlflow.set_tag("release.version", "2.2.0")



