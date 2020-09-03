#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#register_model_uri
#
import warnings
from pprint import pprint
import sys
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    if (len (sys.argv) !=2):
        print("usage: need run_id as an argument")
        sys.exit(1)

    local_store_uri = "sqlite:///api_mlruns.db"
    mlflow.set_tracking_uri(local_store_uri)

    model_uri = "runs:/{}".format(sys.argv[1])
    mv = mlflow.register_model(model_uri, "RandomForestRegressionModel")
    pprint("Registered Model Version Info={}".format(mv))

