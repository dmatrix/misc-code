import warnings
import os
import sys
import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    if len(sys.argv) != 3:
        print("usage: {} <experiment_id> <runid>".format(os.path.basename(__file__)))
        sys.exit(1)
    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    print(f"Running local model registry={local_registry}")
    exp_id = int(sys.argv[1])
    run_id = sys.argv[2]
    filter_runid = "tags.my_runid='{}'".format(run_id)

    mlflow.set_tracking_uri(local_registry)

    client = MlflowClient()
    # Get all versions of the model filtered by name
    results = client.search_runs(exp_id, filter_runid)
    print("-" * 80)
    for res in results:
        print("RunData={}".format(res.data))
