from mlflow.tracking import MlflowClient

if __name__ == '__main__':

    # Case-sensitive name
    client = MlflowClient()
    experiment = client.get_experiment_by_name("Default")

    # Show experiment info
    print("Name: {}".format(experiment.name))
    print("Experiment ID: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))
