import os

from ray import tune
from ray.tune.integration.mlflow import mlflow_mixin
import mlflow


def get_tracking_uri():
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI', "sqlite:///mlruns.db")
    return tracking_uri


def create_mlflow_experiment(exp_name):
    exp = mlflow.get_experiment_by_name(exp_name)
    if exp is None:
        mlflow.create_experiment(exp_name)


if __name__ == '__main__':

    mlflow_tracking_uri = get_tracking_uri()
    print(f"mlflow tracking uri: {mlflow_tracking_uri}")

    # Create the Mlflow experiment.
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    os.environ['MLFLOW_TRACKING_URI'] = mlflow_tracking_uri
    create_mlflow_experiment("cuj_experiment")

    @mlflow_mixin
    def train_fn(config):
        for i in range(10):
            loss = config["a"] + config["b"]
            mlflow.log_metric(key="loss", value=loss)
        tune.report(loss=loss, done=True)


    tune.run(
        train_fn,
        config={
            # define search space here
            "a": tune.choice([1, 2, 3]),
            "b": tune.choice([4, 5, 6]),
            # mlflow configuration
            "mlflow": {
                "experiment_name": "cuj_experiment",
                "tracking_uri": mlflow_tracking_uri
            }
        })