#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#delete_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    with mlflow.start_run() as run:
        mlflow.log_param("p", 0)

    run_id = run.info.run_id
    mlflow.delete_run(run_id)
    print("run_id: {}; lifecycle_stage: {}".format(run_id, mlflow.get_run(run_id).info.lifecycle_stage))
