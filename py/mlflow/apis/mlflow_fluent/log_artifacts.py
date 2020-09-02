#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_artifacts
#
import warnings
import json
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create some artifacts data tor preserve
    features = "rooms, zipcode, median_price, school_rating, transport"
    data = [{"state": "TX", "Available": 25, "Type": "Bunglow"},
            {"state": "OR", "Available": 83, "Type": "Condo"}]

    # Create couple of artifact files under the directory "data"
    with open("data/data.json", 'w', encoding='utf-8') as f:
        [json.dump(d, f, indent=4) for d in data]
    with open("data/features.txt", 'w') as f:
        f.write(features)

    # Creates a run if one is not active and write all files
    # in "data" to root artifact_uri/states
    mlflow.log_artifacts("data", artifact_path="states")

    # End the run above
    mlflow.end_run()

    # Or use Context Manager to create a new run
    with mlflow.start_run(run_name="My Runs"):
        mlflow.log_artifacts("data", artifact_path="states")

