#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#set_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Set an experiment name, it must be unique.
    # Experiment names are case sensitive
    mlflow.set_experiment("Social NLP Experiments")

    # Get Experiment Details
    data = mlflow.get_experiment_by_name("Social NLP Experiments")

    # Print the contents of Experiment data
    print("Experiment_id={}".format(data.experiment_id))
    print("Artifact Location={}".format(data.artifact_location))
    print("Tags={}".format(data.tags))
    print("Lifecycle_stage={}".format(data.lifecycle_stage))
