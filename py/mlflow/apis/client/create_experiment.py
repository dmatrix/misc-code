import warnings

import mlflow
from mlflow.tracking import MlflowClient


if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create an experiment name, which must be unique and case sensitive
    client = MlflowClient()
    experiment_id = client.create_experiment("Social NLP Experiments")
    client.set_experiment_tag(experiment_id, "nlp.framework", "Spark NLP")

    # Fetch experiment metadata information
    experiment = client.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))


