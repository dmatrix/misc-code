#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#end_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Start run and get status
    mlflow.start_run()
    run = mlflow.active_run()
    print("run_id: {}; status: {}".format(run.info.run_id, run.info.status))

    # End the run and get status
    mlflow.end_run()
    run = mlflow.get_run(run.info.run_id)
    print("run_id: {}; status: {}".format(run.info.run_id, run.info.status))

