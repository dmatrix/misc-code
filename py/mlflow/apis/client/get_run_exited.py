from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    # The run has finished since we have existed the with block
    # Fetch the run
    client = MlflowClient()
    run = client.get_run("a84139e4f98046cbbf1bcf185c30f744")
    print("run_id: {}".format(run.info.run_id))
    print("metrics: {}".format(run.data.metrics))
    print("status: {}".format(run.info.status))
