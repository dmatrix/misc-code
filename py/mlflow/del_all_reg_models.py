import sys
import pprint
import mlflow
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")
    #model_name = "sk-learn-random-forest-reg-model"
    mode_name="WeatherForecastModel"
    #
    # Get model name if not registered, register with model registry
    # on a local host
    #
    client = MlflowClient()
    client.delete_registered_model("WeatherForecastModel")
    print("=" * 80)
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_model_versions("name='WeatherForecastModel'")]
