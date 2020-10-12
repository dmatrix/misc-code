from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_artifact_info(artifact):
        print("artifact: {}".format(artifact.path))
        print("is_dir: {}".format(artifact.is_dir))
        print("size: {}".format(artifact.file_size))

    features = "rooms zipcode, median_price, school_rating, transport"
    labels = "price"

    # Create a run under the default experiment (whose id is "0").
    client = MlflowClient()
    experiment_id = "0"
    run = client.create_run(experiment_id)

    # Create some artifacts and log under the above run
    for file, content in [("features", features), ("labels", labels)]:
        with open("{}.txt".format(file), 'w') as f:
            f.write(content)
        client.log_artifact(run.info.run_id, "{}.txt".format(file))

    # Fetch the logged artifacts
    artifacts = client.list_artifacts(run.info.run_id)
    for artifact in artifacts:
        print_artifact_info(artifact)
    client.set_terminated(run.info.run_id)





