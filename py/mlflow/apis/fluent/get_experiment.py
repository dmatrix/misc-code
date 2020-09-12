#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Convert experiment ID as a string argument
    experiment = mlflow.get_experiment("0")

    # Print the contents of Experiment data
    print("Name: {}".format(experiment.name))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))




