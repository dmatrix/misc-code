import mlflow
from mlflow.tracking._tracking_service import utils
import os

if __name__ == "__main__":

    mlflow.set_tracking_uri('databricks')
    # Note: get_host_creds will be undefined if not logging to a remote tracking server, e.g. if logging to the local filesystem
    host_creds = utils._get_store().get_host_creds()
    token = host_creds.token
    host = host_creds.host
    print(host, token, os.getgid())

