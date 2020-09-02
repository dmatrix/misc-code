#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.active_run
#
import warnings
from pprint import pprint
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    params = {"learning_rate": 0.01, "n_estimators": 10}
    metrics = {"mse": 2500.00, "rmse": 50.00}
    tags = {"engineering": "ML Platform",
            "release.candidate": "RC1",
            "release.version": "2.2.0"}

    # Creates a run if one is not active and log two parameters
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.set_tags(tags)

    client = mlflow.tracking.MlflowClient()
    data = client.get_run(mlflow.active_run().info.run_id).data

    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    metrics = {k: v for k, v in data.metrics.items()}
    params = {k: v for k, v in data.params.items()}

    print("-" * 50)
    pprint(params)
    pprint(metrics)
    pprint(tags)


