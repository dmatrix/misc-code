#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#delete_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    experiment_id = mlflow.create_experiment("New Experiment3")
    mlflow.delete_experiment(experiment_id)

    # Examine the deleted experiment details. Deleted experiments
    # are moved to a .thrash folder under the artifact location top
    # level directory.
    experiment = mlflow.get_experiment(experiment_id)

    # Print the contents of deleted Experiment data
    print("Name: {}".format(experiment.name))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))
