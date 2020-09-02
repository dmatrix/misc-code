#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Convert experiment ID as a string argument
    data = mlflow.get_experiment(str(0))

    # Print the contents of Experiment data
    print("Name={}".format(data.name))
    print("Artifact Location={}".format(data.artifact_location))
    print("Tags={}".format(data.tags))
    print("Lifecycle_stage={}".format(data.lifecycle_stage))




