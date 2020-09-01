#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#delete_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Convert experiment ID as a string argument
    mlflow.delete_experiment(str(1))

    # Examine the deleted experiment details. Deleted experiments
    # are moved to a .thrash folder under the artifact location top
    # level directory.
    data = mlflow.get_experiment(str(1))

    # Print the contents of deleted Experiment data
    print("Name={}".format(data.name))
    print("Artifact Location={}".format(data.artifact_location))
    print("Tags={}".format(data.tags))
    print("Lifecycle_stage={}".format(data.lifecycle_stage))
