#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_artifacts
#
import warnings
import os
import json
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create some artifacts data to preserve
    features = "rooms, zipcode, median_price, school_rating, transport"
    data = {"state": "TX", "Available": 25, "Type": "Detached"}

    # Create couple of artifact files under the directory "data"
    os.makedirs("data", exist_ok=True)
    with open("data/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    with open("data/features.txt", 'w') as f:
        f.write(features)

    # Write all files in "data" to root artifact_uri/states
    with mlflow.start_run():
        mlflow.log_artifacts("data", artifact_path="states")

