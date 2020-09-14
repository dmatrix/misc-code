#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#list_run_info
#
import warnings
import mlflow
from mlflow.entities import ViewType

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create two runs
    with mlflow.start_run() as run1:
        mlflow.log_param("p", 0)
        mlflow.log_metric("click_rate", 1.55)

    with mlflow.start_run() as run2:
        mlflow.log_param("p", 0)
        mlflow.log_metric("click_rate", 2.50)

    # Delete the last run
    mlflow.delete_run(run2.info.run_id)

    def print_run_infos(run_infos):
        for r in run_infos:
            print("- run_id: {}, lifecycle_stage: {}".format(r.run_id, r.lifecycle_stage))

    print("Active runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ACTIVE_ONLY))

    print("Deleted runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.DELETED_ONLY))

    print("All runs:")
    print_run_infos(mlflow.list_run_infos("0", run_view_type=ViewType.ALL, order_by=["metric.click_rate DESC"]))
