import warnings

from mlflow.tracking import MlflowClient

if __name__ == '__main__':

    warnings.filterwarnings("ignore")

    # Create a run under an experiment whose default ID is "0".
    client = MlflowClient()
    expirement_id = "0"
    run = client.create_run(expirement_id)
    run_id = run.info.run_id
    print("run_id: {}; lifecycle_stage: {}".format(run_id, run.info.lifecycle_stage))
    print("--")
    client.delete_run(run_id)
    del_run = client.get_run(run_id)
    print("run_id: {}; lifecycle_stage: {}".format(run_id, del_run.info.lifecycle_stage))
