import pprint
import mlflow
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    print(f"Running local model registry={local_registry}")
    model_name="WeatherForecastModel"
    run_id = "6e3f1e529f5943809e6acb9d7259d3ca"
    filter_name = "name='{}'".format(model_name)
    filter_runid= "run_id='{}'".format(run_id)

    mlflow.set_tracking_uri(local_registry)

    # Search and filter by name
    print(f"List of all versions of model_name={model_name} model")
    print("=" * 80)
    client = mlflow.tracking.MlflowClient()
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_model_versions(filter_name)]
    # Search and filter by run_id
    print(f"Search of all versions of run_id={run_id} model")
    print("-" * 80)
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_model_versions(filter_runid)]

    # get the maximum version
    #model_versions = client.search_registered_models("name='WeatherForecastModel'")
    #max_model_version = max([model_version.version for model_version in model_versions])
    #print(f"max_version = {max_model_version}")
    #print(f"max_version type is = {type(max_model_version)}")

    model_name = "WeatherForecastModel"
    run_id = "6e3f1e529f5943809e6acb9d7259d3ca"
    filter_name = "name='{}'".format(model_name)
    filter_runid = "run_id='{}'".format(run_id)
    client = mlflow.tracking.MlflowClient()
    # Get all versions of the model filtered by name
    results = client.search_model_versions(filter_name)
    print("=" * 80)
    print(results)
    # Get the version of the model filtered by run_id
    print("=" * 80)
    results = client.search_model_versions(filter_runid)
    print(results)
