#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.delete_tag
#
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Creates a run if one is not active and deletes the tag
    mlflow.delete_tag("engineering", "ML Platform")

    # end the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.delete_tag("engineering", "ML Platform")



