import warnings
import os
import sys
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    if len(sys.argv) != 3:
        print("usage: {} <model_name> <runid>".format(os.path.basename(__file__)))
        sys.exit(1)
    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    print(f"Running local model registry={local_registry}")
    model_name = sys.argv[1]
    run_id = sys.argv[2]

    mlflow.set_tracking_uri(local_registry)
    client = mlflow.tracking.MlflowClient()

    # Get all versions of the model filtered by name
    model_name = sys.argv[1]
    filter_name = "name='{}'".format(model_name)
    results = client.search_model_versions(filter_name)
    print("-" * 80)
    for res in results:
        print("name={}; run_id={}; version={}".format(res.name, res.run_id, res.version))

    # Get the version of the model filtered by run_id
    run_id = sys.argv[2]
    filter_runid = "run_id='{}'".format(run_id)
    print("-" * 80)
    results = client.search_model_versions(filter_runid)
    for res in results:
        print("name={}; run_id={}; version={}".format(res.name, res.run_id, res.version))
