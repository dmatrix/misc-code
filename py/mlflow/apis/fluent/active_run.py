#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.active_run
#
import warnings
from pprint import pprint
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    mlflow.start_run()

    mlflow.log_param("p", 0)
    mlflow.log_metric("m", 1)
    mlflow.set_tag("t", 2)

    client = mlflow.tracking.MlflowClient()
    data = client.get_run(mlflow.active_run().info.run_id).data

    # Extract only user defined tags; skip System tags starting with "mlflow."
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}

    pprint(data.params)
    pprint(data.metrics)
    pprint(tags)

    mlflow.end_run()


