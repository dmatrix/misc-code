import warnings

from mlflow.tracking import MlflowClient

if __name__ == '__main__':

    warnings.filterwarnings("ignore")

    client = MlflowClient()
    run = client.create_run("0")
    run_id = run.info.run_id
    print("run_id: {}; lifecycle_stage: {}".format(run_id, run.info.lifecycle_stage))
    client.delete_run(run_id)
    del_run = client.get_run(run_id)
    print("run_id: {}; lifecycle_stage: {}".format(run_id, del_run.info.lifecycle_stage))
    client.restore_run(run_id)
    restore_run = client.get_run(run_id)
    print("run_id: {}; lifecycle_stage: {}".format(run_id, restore_run.info.lifecycle_stage))
