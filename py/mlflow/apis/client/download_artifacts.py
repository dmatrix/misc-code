import os
import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    # Log artifacts
    with mlflow.start_run() as run:
        mlflow.log_artifact("features.txt", artifact_path="features")

    client = MlflowClient()
    local_dir = "/tmp/artifact_downloads"
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)
    local_path = client.download_artifacts(run.info.run_id, "features", local_dir)
    print("Artifacts downloaded at : {}".format(local_path))
    print("Artifacts: {}".format(os.listdir(local_path)))
