#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_tracking_uri
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Get the current tracking uri
    tracking_uri = mlflow.get_tracking_uri()
    print("Current run's tracking uri={}".format(tracking_uri))

