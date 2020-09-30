import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    with mlflow.start_run() as run:
        mlflow.log_param("p", 0)

    # The run has finished since we have existed the with block
    # Fetch the run
    client = MlflowClient()
    run = client.get_run(run.info.run_id)
    print("run_id: {}".format(run.info.run_id))
    print("params: {}".format(run.data.params))
    print("status: {}".format(run.info.status))
