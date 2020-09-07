#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_experement_by_name
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Case-sensitive name
    experiment = mlflow.get_experiment_by_name("Default")

    # Print the contents of Experiment data
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))




