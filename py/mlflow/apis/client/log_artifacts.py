import os
import json

from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    # Create some artifacts data to preserve
    features = "rooms, zipcode, median_price, school_rating, transport"
    data = {"state": "TX", "Available": 25, "Type": "Detached"}

    # Create couple of artifact files under the directory "data"
    os.makedirs("data", exist_ok=True)
    with open("data/data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    with open("data/features.txt", 'w') as f:
        f.write(features)

    # Create a run under the default experiment (whose id is "0"), and log
    # all files in "data" to root artifact_uri/states
    client = MlflowClient()
    expermient_id = "0"
    run = client.create_run(expermient_id)
    client.log_artifacts(run.info.run_id, "data", artifact_path="states")
    artifacts = client.list_artifacts(run.info.run_id)
    for artifact in artifacts:
        print("artifact: {}".format(artifact.path))
        print("is_dir: {}".format(artifact.is_dir))
    client.set_terminated(run.info.run_id)


