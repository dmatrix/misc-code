import warnings

from mlflow.tracking import MlflowClient


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    def print_experiment_info(experiment):
        print("Name: {}".format(experiment.name))
        print("Experiment_id: {}".format(experiment.experiment_id))
        print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    # Create an experiment name, which must be unique and case sensitive
    client = MlflowClient()
    experiment_id = client.create_experiment("Social NLP Experiments")

    # Fetch experiment metadata information
    experiment = client.get_experiment(experiment_id)
    print_experiment_info(experiment)
    print("--")

    # Rename and fetch experiment metadata information
    client.rename_experiment(experiment_id, "Social Media NLP Experiments")
    experiment = client.get_experiment(experiment_id)
    print_experiment_info(experiment)
