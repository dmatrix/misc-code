import torch
import torch.nn as nn

import mlflow.pytorch
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":

    class PyTorchModel(nn.Module):
        def __init__(self, n_input_features):
            super(PyTorchModel, self).__init__()
            self._n_input_features = n_input_features
            self._linear = nn.Linear(n_input_features, 1)

        @property
        def input_features(self):
            return self._n_input_features

        def forward(self, x):
            y_pred = torch.sigmoid(self._linear(x))
            return y_pred

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    name = "PyTorchLinearModel"
    model = PyTorchModel(10)

    # Log MLflow entities
    with mlflow.start_run() as run:
        mlflow.log_param("input_features", 10)
        mlflow.pytorch.log_model(model, artifact_path="models/pytorch-model")

    # Register model name in the model registry
    client = MlflowClient()
    client.create_registered_model(name)

    # Create a new version of the rfr model under the registered model name
    desc = "A new version of the PyTorch model"
    model_uri = "runs:/{}/models/pytorch-model".format(run.info.run_id)
    mv = client.create_model_version(name, model_uri, run.info.run_id, description=desc)
    print("Name: {}".format(mv.name))
    print("Version: {}".format(mv.version))
    print("Description: {}".format(mv.description))
    print("Status: {}".format(mv.status))
    print("Stage: {}".format(mv.current_stage))
