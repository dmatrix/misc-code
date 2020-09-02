#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#set_tracking_uri
#
import warnings
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Get tracking uri
    tracking_uri = mlflow.get_tracking_uri()
    print("Current tracking uri={}".format(tracking_uri))
    mlflow.end_run()

    mlflow.set_tracking_uri("file:///tmp/my_tracking")
    tracking_uri = tracking_uri = mlflow.get_tracking_uri()
    print("Current tracking uri={}".format(tracking_uri))
