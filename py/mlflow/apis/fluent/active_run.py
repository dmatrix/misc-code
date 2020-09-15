#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.active_run
#
import warnings
from pprint import pprint
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    mlflow.start_run()
    run = mlflow.active_run()
    print("Active run_id: {}".format(run.info.run_id))
    mlflow.end_run()


