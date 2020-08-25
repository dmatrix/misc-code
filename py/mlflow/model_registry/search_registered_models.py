import pprint
import warnings

import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")
    model_name="IrisClassifierModel"
    filter_string = "name='{}'".format(model_name)
    # Search model versions
    print(f"List of all versions of {model_name} model")
    print("=" * 80)
    client = mlflow.tracking.MlflowClient()
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_registered_models(filter_string=filter_string)]
    print("=" * 80)
    # Search all registered models and return by ascending order
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_registered_models(order_by=["name ASC"])]

    model_name = "IrisClassifierModel"
    filter = "name='{}'".format(model_name)
    client = mlflow.tracking.MlflowClient()
    # Get search results filtered by the registered model name
    results = client.search_registered_models(filter_string=filter)
    print("--" * 80)
    print(results)
    # Get all registered models and order them by ascending order of the registered model names
    results = client.search_registered_models(order_by=["name ASC"])
    print("--" * 80)
    print(results)

