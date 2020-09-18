#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#search_runs
#
import warnings
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Create an experiment and log two runs under it
    experiment_id = mlflow.create_experiment("Social NLP Experiments")
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_metric("m", 1.55)
        mlflow.set_tag("s.release", "1.1.0-RC")
    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_metric("m", 2.50)
        mlflow.set_tag("s.release", "1.2.0-GA")

    # Search all runs in experiment_id
    df = mlflow.search_runs([experiment_id], order_by=["metrics.m DESC"])

    # Print pandas DataFrame's rows and columns
    print(df.loc[:, ["metrics.m", "tags.s.release", "run_id"]].to_string())
    print("--")

    # Search the experiment_id using a filter_string with tag
    # that has a case insensitive pattern
    filter_string = "tags.s.release ILIKE '%rc%'"
    df = mlflow.search_runs([experiment_id], filter_string=filter_string)

    # Print pandas DataFrame's rows and columns
    print(df.loc[:, ["metrics.m", "tags.s.release", "run_id"]].to_string())
