import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == '__main__':

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    tags = {"engineering": "ML Platform"}
    client = MlflowClient()
    run = client.create_run("0", tags=tags)

    # Show newly created run metadata and info
    print("Run tags: {}".format(run.data.tags))
    print("Experiment id: {}".format(run.info.experiment_id))
    print("Run id: {}".format(run.info.run_id))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
    print("status: {}".format(run.info.status))
