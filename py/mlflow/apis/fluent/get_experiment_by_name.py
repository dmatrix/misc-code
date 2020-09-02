#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_experement_by_name
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Case-sensitive name
    data = mlflow.get_experiment_by_name("Default")

    # Print the contents of Experiment data
    print("Experiment_id={}".format(data.experiment_id))
    print("Artifact Location={}".format(data.artifact_location))
    print("Tags={}".format(data.tags))
    print("Lifecycle_stage={}".format(data.lifecycle_stage))




