#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_artifact
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    # Creates a run if one is not active and write this file
    # in a directory "features" under the root artifact_uri/features
    mlflow.log_artifact("features.txt", artifact_path="features")

    # End the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.log_artifact("features.txt", artifact_path="features")




