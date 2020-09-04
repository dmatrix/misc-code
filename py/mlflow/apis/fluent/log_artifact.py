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

    # With artifact_path=None write all files under
    # root artifact_uri/artifacts directory
    with mlflow.start_run():
        mlflow.log_artifact("features.txt")




