import mlflow
from mlflow.tracking import MlflowClient


def print_run_info(r):
    print("run_id: {}".format(r.info.run_id))
    print("lifecycle_stage: {}".format(r.info.lifecycle_stage))
    print("status: {}".format(run.info.status))
    print("params: {}".format(r.data.params))


if __name__ == '__main__':

    with mlflow.start_run() as run:
        mlflow.log_param("m1", 1)

    # This ends this run
    run = mlflow.get_run(run.info.run_id)
    print_run_info(run)


    # Now update the ended run using the CRUD MLFlowClient APIs
    client = MlflowClient()
    client.log_param(run.info.run_id, "m1", 2)
    print("--" * 2)
    print_run_info(run)
