import warnings
import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    # Create an experiment name, which must be unique and case sensitive
    client = MlflowClient()
    experiment_id = client.create_experiment("New Experiment1")
    client.delete_experiment(experiment_id)

    # Examine the deleted experiment details. Deleted experiments
    # are moved to a .trash folder under the artifact URI location top
    # level directory.
    experiment = client.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))
