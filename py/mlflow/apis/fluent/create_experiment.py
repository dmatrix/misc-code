#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#create_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create an experiment name, which must be unique and case sensitve
    experiment_id = mlflow.create_experiment("Social NLP Experiments")

    # Convert experiment ID as a string argument and fetch its data
    experiment = mlflow.get_experiment(str(experiment_id))

    # Print the contents of Experiment data
    print("Name={}".format(experiment.name))
    print("Experiment_id={}".format(experiment.experiment_id))
    print("Artifact Location={}".format(experiment.artifact_location))
    print("Tags={}".format(experiment.tags))
    print("Lifecycle_stage={}".format(experiment.lifecycle_stage))
