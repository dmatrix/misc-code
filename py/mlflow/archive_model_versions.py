import sys
import pprint
import mlflow
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    if (len(sys.argv) < 2):
        print("Usage: list of versions to archive for the model")
        sys.exit(1)

    # set the tracking server to be Databricks Community Edition
    # set the experiment name; if name does not exist, MLflow will
    # create one for you
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")
    model_name = "sk-learn-random-forest-reg-model"
    version = int(sys.argv[1])
    #
    # Get model name if not regisered, register with model registry
    # on a local host
    #
    client = MlflowClient()
    for version in sys.argv[1:]:
        client.transition_model_version_stage(
            name="sk-learn-random-forest-reg-model",
            version=int(version),
            stage="archived")
    print("=" * 80)
    [pprint.pprint(dict(mv), indent=4) for mv in client.search_model_versions("name='sk-learn-random-forest-reg-model'")]
