import numpy as np
from pathlib import Path

import mlflow
from mlflow.models import Model

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import mean_squared_error
from mlflow.tracking.artifact_utils import _download_artifact_from_uri


def print_model_info(m_uri, x):
    loaded_model = mlflow.sklearn.load_model(m_uri)
    res = loaded_model.predict(x)
    print("model_uri: {}".format(m_uri))
    print("model predictions: {}".format(res))


if __name__ == "__main__":
    # Enable auto-logging
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    mlflow.sklearn.autolog()

    # Load data
    iris_dataset = load_iris()
    data, target, target_names = (
        iris_dataset["data"],
        iris_dataset["target"],
        iris_dataset["target_names"],
    )

    # Instantiate model
    model = GradientBoostingClassifier()

    # Split training and validation data
    np.random.shuffle(data)
    np.random.shuffle(target)
    train_x, train_y = data[:100], target[:100]
    val_x, val_y = data[100:], target[100:]

    # Train and evaluate model
    with mlflow.start_run() as run:
        model.fit(train_x, train_y)
    print("MSE:", mean_squared_error(model.predict(val_x), val_y))
    print("Target names: ", target_names)
    print("run_id: {}".format(run.info.run_id))

    # Registered the auto-logged model.
    model_uri = "runs:/{}/model".format(run.info.run_id)
    registered_model_name = "RayMLflowIntegration"
    mv = mlflow.register_model(model_uri, registered_model_name)
    print("Name: {}".format(mv.name))
    print("Version: {}".format(mv.version))

    # load the model with runs://URI
    print_model_info(model_uri, val_x)
    print("--" * 20)
    # load the model using models:URI
    model_uri = "models:/{}/1".format(registered_model_name)
    print_model_info(model_uri, val_x)
    print("--" * 20)

    # Use plugin code to load the model config
    path = Path(_download_artifact_from_uri(model_uri))
    model_config = path / 'MLmodel'
    model_config = Model.load(model_config)
    print("model_uri: {}".format(model_uri))
    print("model_config: {}".format(model_config))
    print(model_config)
