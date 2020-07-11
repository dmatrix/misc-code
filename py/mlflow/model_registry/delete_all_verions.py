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
    model_name = "WeatherForecastModel"
    client = MlflowClient()

    # Get all versions of this model and transition them to Archive for deletion
    model_versions = client.search_model_versions("name='WeatherForecastModel'")
    if model_versions:
        for mv in model_versions:
            client.transition_model_version_stage(
                name="WeatherForecastModel",
                version=mv.version,
                stage="archived")

        # Delete this registered model
        client.delete_registered_model("WeatherForecastModel")
