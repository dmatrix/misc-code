from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    # The run has finished since we have existed the with block
    # Fetch the run
    client = MlflowClient()
    run = client.get_run("ca6197a6dbb14417a0321c1f7fef7ed3")
    print("run_id: {}".format(run.info.run_id))
    print("params: {}".format(run.data.params))
    print("status: {}".format(run.info.status))
