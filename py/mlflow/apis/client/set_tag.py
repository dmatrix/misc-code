import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    def print_run_info(run):
        print("run_id: {}".format(run.info.run_id))
        print("Tags: {}".format(run.data.tags))

    # Create a run under the default experiment (whose id is "0").
    client = MlflowClient()
    experiment_id = "0"
    run = client.create_run(experiment_id)
    print_run_info(run)
    print("--")

    # Set a tag and fetch update run info
    client.set_tag(run.info.run_id, "nlp.framework", "Spark NLP")
    run = client.get_run(run.info.run_id)
    print_run_info(run)
