import warnings

import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create an experiment and set its tag
    client = MlflowClient()
    experiment_id = client.create_experiment("Social Media NLP Experiments")
    client.set_experiment_tag(experiment_id, "nlp.framework", "Spark NLP")

    # Fetch experiment metadata information
    experiment = client.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Tags: {}".format(experiment.tags))
