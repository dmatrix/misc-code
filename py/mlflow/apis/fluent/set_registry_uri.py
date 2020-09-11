#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#set_registry_uri
#
import warnings
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    mlflow.set_registry_uri("sqlite:///tmp/registry.db")
    mr_uri = mlflow.get_registry_uri()
    print("Current registry uri={}".format(mr_uri))
    tracking_uri = mlflow.get_tracking_uri()
    print("Current tracking uri: {}".format(tracking_uri))

    assert tracking_uri != mr_uri
