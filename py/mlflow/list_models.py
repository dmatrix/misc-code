import pprint

import mlflow.sklearn
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    print(f"Running local model registry={local_registry}")
    model_name="WeatherForecastModel"
    mlflow.set_tracking_uri(local_registry)

    clnt = MlflowClient()
    # Get a list of all registered models
    print("List of all registered models")
    print("=" * 80)
    [print(pprint.pprint(dict(rm), indent=4)) for rm in clnt.list_registered_models()]
