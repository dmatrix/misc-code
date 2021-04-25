import warnings

import numpy as np
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LinearRegression
from mlflow.models.signature import infer_signature

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    def print_auto_logged_info(r):
        tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
        artifacts = [f.path for f in MlflowClient().list_artifacts(r.info.run_id, "model")]
        print("run_id: {}".format(r.info.run_id))
        print("artifacts: {}".format(artifacts))
        print("params: {}".format(r.data.params))
        print("metrics: {}".format(r.data.metrics))
        print("tags: {}".format(tags))

    # prepare training data
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3


    model = LinearRegression()
    with mlflow.start_run() as run:
        model.fit(X, y)
        model_signature = infer_signature(X, model.predict(X))
        mlflow.sklearn.log_model(model, "models", signature=model_signature)

    # fetch the auto logged parameters and metrics
    print_auto_logged_info(mlflow.get_run(run_id=run.info.run_id))
