#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_artifact_uri
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    # Use context manager to create a run and log the artifact
    # in a directory "features" under the root artifact_uri/features
    with mlflow.start_run():
        mlflow.log_artifact("features.txt", artifact_path="features")

        # Fetch the artifact uri
        artifact_uri = mlflow.get_artifact_uri()
        print("Artifact uri: {}".format(artifact_uri))

        # Fetch a specific artifact uri
        artifact_uri = mlflow.get_artifact_uri(artifact_path="features/features.txt")
        print("Artifact uri: {}".format(artifact_uri))




