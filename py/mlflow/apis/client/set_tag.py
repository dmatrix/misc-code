import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create a run under the default experiment 0
    client = MlflowClient()
    run = client.create_run("0")
    print("run_id: {}".format(run.info.run_id))
    print("Tags: {}".format(run.data.tags))
    print("--")

    # Set a tag and fetch new info
    client.set_tag(run.info.run_id, "nlp.framework", "Spark NLP")
    run = client.get_run(run.info.run_id)
    print("run_id: {}".format(run.info.run_id))
    print("Tags: {}".format(run.data.tags))
