import warnings
import sys
import os
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    if len(sys.argv) != 2:
        print("usage: {} <model_name>".format(os.path.basename(__file__)))
        sys.exit(1)
    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    print(f"Running local model registry={local_registry}")
    mlflow.set_tracking_uri(local_registry)
    client = mlflow.tracking.MlflowClient()

    # Get search results filtered by the registered model name
    model_name = sys.argv[1]
    filter_string = "name='{}'".format(model_name)
    results = client.search_registered_models(filter_string=filter_string)
    print("-" * 80)
    for res in results:
        for mv in res.latest_versions:
            print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))
    print("-" * 80)

    # Get search results filtered by the registered model name that matches
    # prefix pattern
    filter_string = "name LIKE 'Azure%'"
    results = client.search_registered_models(filter_string=filter_string)
    for res in results:
        for mv in res.latest_versions:
            print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))

    # Get all registered models and order them by ascending order of the registered model names
    results = client.search_registered_models(order_by=["name ASC"])
    print("-" * 80)
    for res in results:
        for mv in res.latest_versions:
            print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))
