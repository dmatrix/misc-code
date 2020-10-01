from mlflow.tracking import MlflowClient

if __name__ == '__main__':

    client = MlflowClient()
    exp_id = client.create_experiment("Experiment")
    experiment = client.get_experiment(exp_id)

    # Show experiment info
    print("Name: {}".format(experiment.name))
    print("Experiment ID: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))
