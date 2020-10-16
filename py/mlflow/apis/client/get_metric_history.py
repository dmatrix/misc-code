from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_metric_info(m):
        print("name: {}".format(m.key))
        print("value: {}".format(m.value))
        print("timestamp: {}".format(m.timestamp))

    # Create a run under the default experiment (whose id is "0"). Since this is low-level
    # CRUD operation, the method will create a run. To end the run, you'll have
    # to explicitly end it.
    client = MlflowClient()
    experiment_id = "0"
    run = client.create_run(experiment_id)
    print("run_id: {}".format(run.info.run_id))
    print("--")

    # Log couple of metrics, update their initial value, and fetch each
    # logged metrics' history.
    for k, v in [("m1", 1.5), ("m2", 2.5)]:
        client.log_metric(run.info.run_id, k, v)
        client.log_metric(run.info.run_id, k, v+1)
        history = client.get_metric_history(run.info.run_id, k)
        for m in history:
            print_metric_info(m)
            print("--")
    client.set_terminated(run.info.run_id)
