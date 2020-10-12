from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    # The run has finished since we have exited the with block
    # Fetch the run
    client = MlflowClient()
    client.log_param("ca6197a6dbb14417a0321c1f7fef7ed3", "p", 1)
    client.log_param("ca6197a6dbb14417a0321c1f7fef7ed3", "p2", 2)

    run = client.get_run("ca6197a6dbb14417a0321c1f7fef7ed3")
    print("run_id: {}".format(run.info.run_id))
    print("params: {}".format(run.data.params))
    print("status: {}".format(run.info.status))
