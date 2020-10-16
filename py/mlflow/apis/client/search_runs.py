import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

if __name__ == "__main__":

    def print_run_info(runs):
        for r in runs:
            tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
            print("run_id: {}".format(r.info.run_id))
            print("lifecycle_stage: {}".format(r.info.lifecycle_stage))
            print("metrics: {}".format(r.data.metrics))

            # Exclude mlflow tags
            tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
            print("tags: {}".format(tags))

    # Create an experiment and log two runs with metrics and tags under it
    experiment_id = mlflow.create_experiment("Social NLP Experiments")
    with mlflow.start_run(experiment_id=experiment_id) as run:
        mlflow.log_metric("m", 1.55)
        mlflow.set_tag("s.release", "1.1.0-RC")
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_metric("m", 2.50)
        mlflow.set_tag("s.release", "1.2.0-GA")

    # Search all runs under experiment id and order by descending value of the metric 'm'
    client = MlflowClient()
    runs = client.search_runs(experiment_id, order_by=["metrics.m DESC"])
    print_run_info(runs)
    print("--")

    # Delete the first run
    client.delete_run(run_id=run.info.run_id)

    # Search only deleted runs under the experiment_id and use a case insensitive pattern
    # in the filter_string for the tag.
    filter_string = "tags.s.release ILIKE '%rc%'"
    runs = client.search_runs(experiment_id, run_view_type=ViewType.DELETED_ONLY, filter_string=filter_string)
    print_run_info(runs)
