import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    def print_run_info(run):
        print("run_id: {}".format(run.info.run_id))
        print("Tags: {}".format(run.data.tags))

    # Create a run with some tags under the default experiment id "0"
    client = MlflowClient()
    tags = {"t1": 1, "t2": 2}
    experimnent_id = "0"
    run = client.create_run(experimnent_id, tags=tags)
    print_run_info(run)
    print("--")

    # Delete tag and fetch new info
    client.delete_tag(run.info.run_id, "t1")
    run = client.get_run(run.info.run_id)
    print_run_info(run)
