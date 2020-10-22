import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

if __name__ == "__main__":

    def print_run_infos(run_infos):
        for r in run_infos:
            print("- run_id: {}, lifecycle_stage: {}".format(r.run_id, r.lifecycle_stage))

    # Create two runs
    with mlflow.start_run() as run1:
        mlflow.log_metric("click_rate", 1.55)

    with mlflow.start_run() as run2:
        mlflow.log_metric("click_rate", 2.50)

    # Delete the last run
    client = MlflowClient()
    client.delete_run(run2.info.run_id)

    # Get all runs under the default experiment (whose id is 0)
    print("Active runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ACTIVE_ONLY))

    print("Deleted runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.DELETED_ONLY))

    print("All runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ALL, order_by=["metric.click_rate DESC"]))
