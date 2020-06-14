import sys
import pprint
import mlflow
from mlflow.tracking import MlflowClient
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)
    if(len(sys.argv) < 2):
        print("Usage: model_name, model_name2...")
        sys.exit(1)

    # set the tracking server to be localhost with sqlite as tracking store
    local_registry = "sqlite:///mlruns.db"
    mlflow.set_tracking_uri(local_registry)
    print(f"Running local model registry={local_registry}")
    
    # Delete the registered model namme
    client = MlflowClient()
    for mname in sys.argv[1:]:
        print(f"Deleting model {mname} and all its versions and data")
        client.delete_registered_model(mname)
    print("=" * 80)
    [print(pprint.pprint(dict(rm), indent=4)) for rm in client.list_registered_models()]
