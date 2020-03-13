import sys
import pprint
import mlflow
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    if (len(sys.argv) < 3):
        print("Usage: model_old_name, model_new_name2...")
        sys.exit(1)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")

    # Delete the registered model namme
    client = MlflowClient()
    old_model_name = sys.argv[1]
    new_model_name = sys.argv[2]
    client.rename_registered_model(old_model_name,new_model_name)
    print("=" * 80)
    [print(pprint.pprint(dict(rm), indent=4)) for rm in client.list_registered_models()]
