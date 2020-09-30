#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    with mlflow.start_run() as run:
        mlflow.log_param("p", 0)

    run_id = run.info.run_id
    run = mlflow.get_run(run_id)
    print("run_id: {}".format(run_id))
    print("lifecycle_stage: {}".format(run.info.lifecycle_stage))
    print("params: {}".format(run.data.params))
