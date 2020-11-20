import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":

    def print_model_version_info(mv):
        print("Name: {}".format(mv.name))
        print("Version: {}".format(mv.version))
        print("Tags: {}".format(mv.tags))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    params = {"n_estimators": 3, "random_state": 42}
    name = "RandomForestRegression"
    rfr = RandomForestRegressor(**params).fit([[0, 1]], [1])

    # Log MLflow entities
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    # Register model name in the model registry
    client = MlflowClient()
    client.create_registered_model(name)

    # Create a new version of the rfr model under the registered model name
    # and set a tag
    model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
    mv = client.create_model_version(name, model_uri, run.info.run_id)
    print_model_version_info(mv)
    print("--")
    client.set_model_version_tag(name, mv.version, "t", "1")
    mv = client.get_model_version(name, mv.version)
    print_model_version_info(mv)
