#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#delete_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Set existing run_ids to delete
    run_ids = ["9010b659f83142938e21dc2baa8fcbe8"]

    # Delete run_ids and fetch the results.
    # Note that runs are not actually delete, only lifecycle stage is set to "deleted"
    [mlflow.delete_run(run_id) for run_id in run_ids]
    [print("run_id={}; lifecycle_stage={}".format(run_id, mlflow.get_run(run_id).info.lifecycle_stage))
        for run_id in run_ids]
