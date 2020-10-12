import time

from mlflow.tracking import MlflowClient
from mlflow.entities import Metric, Param, RunTag
from mlflow.exceptions import MlflowException

if __name__ == "__main__":

    def print_run_info(r):
        print("run_id: {}".format(r.info.run_id))
        print("params: {}".format(r.data.params))
        print("metrics: {}".format(r.data.metrics))
        print("tags: {}".format(r.data.tags))
        print("status: {}".format(r.info.status))


    # Create MLflow entities and a run under the default experiment (whose id is "0").
    timestamp = int(time.time() * 1000)
    metrics = [Metric('m', 1.5, timestamp, 1)]
    params = [Param("p", 'p')]
    tags = [RunTag("t", "t")]
    experiment_id = "0"
    client = MlflowClient()
    run = client.create_run(experiment_id)

    # Log entities, terminate the run, and fetch run status
    client.log_batch(run.info.run_id, metrics=metrics, params=params, tags=tags)
    client.set_terminated(run.info.run_id)
    run = client.get_run(run.info.run_id)
    print_run_info(run)
