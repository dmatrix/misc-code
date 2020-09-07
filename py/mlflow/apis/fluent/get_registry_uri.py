#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_registry_uri
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Get the current model registry uri
    mr_uri = mlflow.get_registry_uri()
    print("Current model registry uri: {}".format(mr_uri))

    # Get the current tracking uri
    tracking_uri = mlflow.get_tracking_uri()
    print("Current tracking uri: {}".format(tracking_uri))

    # They should be the same
    assert(mr_uri == tracking_uri)
