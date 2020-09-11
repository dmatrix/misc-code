#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#end_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Start run and get its run_id and status
    mlflow.start_run()
    run_id = mlflow.active_run().info.run_id
    status = mlflow.get_run(run_id).info.status
    print("run_id: {}; status: {}".format(run_id, status))
    # End the run
    mlflow.end_run()

    # Get final status after the end run
    status = mlflow.get_run(run_id).info.status
    print("run_id: {}; status: {}".format(run_id, status))

