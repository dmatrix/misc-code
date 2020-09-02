#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.set_tags
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    tags = {"engineering": "ML Platform",
            "release.candidate": "RC1",
            "release.version": "2.2.0"}

    # Creates a run if one is not active and set three tags
    mlflow.set_tags(tags)

    # end the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.set_tags(tags)



