import warnings
import mlflow

from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    client = MlflowClient()
    run = client.create_run("0")

    # log and fetch the list of artifacts
    client.log_artifact(run.info.run_id, "features.txt")
    artifacts = client.list_artifacts(run.info.run_id)
    for artifact in artifacts:
        print("artifact: {}".format(artifact.path))
        print("is_dir: {}".format(artifact.is_dir))
    client.set_terminated(run.info.run_id)





