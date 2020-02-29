import sys
import pprint
import mlflow
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    if (len(sys.argv) != 2):
        print("Usage: Need version number for the model")
        sys.exit(1)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")
    #model_name="sk-learn-random-forest-reg-model"
    mode_name="WeatherForecastModel"
    version = int(sys.argv[1])
    #
    # Get model name if not regisered, register with model registry
    # on a local host
    #
    client = MlflowClient()
    client.delete_model_version(
        name="WeatherForecastModel",
        version=version)
    print("=" * 80)
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_model_versions("name='sk-learn-random-forest-reg-model'")]
