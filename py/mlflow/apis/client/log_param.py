from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_run_info(r):
        print("run_id: {}".format(r.info.run_id))
        print("params: {}".format(r.data.params))
        print("status: {}".format(r.info.status))

    # Create a run under the default experiment (whose id is "0"). Since this aisre low-level
    # CRUD operation, this method will create a run. To end the run, you'll have
    # to explicitly end it.
    client = MlflowClient()
    experiment_id = "0"
    run = client.create_run(experiment_id)
    print_run_info(run)
    print("--")

    # Log the parameter. Unlike mlflow.log_param this method
    # does not start a run if one does not exist. It will log
    # the parameter in the backend store
    client.log_param(run.info.run_id, "p", 1)
    client.set_terminated(run.info.run_id)
    run = client.get_run(run.info.run_id)
    print_run_info(run)
