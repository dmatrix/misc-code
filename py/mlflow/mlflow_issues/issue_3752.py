import mlflow

from mlflow.tracking import MlflowClient

if __name__ == '__main__':
    with mlflow.start_run() as run:
        run_id = run.info.run_id

        # logging is ok, no warning
        mlflow.log_metric("metric", True)

    # You can either open the UI and enjoy the "INTERNAL_SERVER_ERROR"
    # or try to retrieve the run for instance:
    MlflowClient().get_run(run_id) # an error is raised
