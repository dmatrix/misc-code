import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":

    def print_model_version_info(mv):
        print("Name: {}".format(mv.name))
        print("Version: {}".format(mv.version))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")

    # Create two runs Log MLflow entities
    with mlflow.start_run() as run1:
        params = {"n_estimators": 3, "random_state": 42}
        rfr = RandomForestRegressor(**params).fit([[0, 1]], [1])
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    with mlflow.start_run() as run2:
        params = {"n_estimators": 6, "random_state": 42}
        rfr = RandomForestRegressor(**params).fit([[0, 1]], [1])
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    # Register model name in the model registry
    name = "RandomForestRegression"
    client = MlflowClient()
    client.create_registered_model(name)

    # Create a two versions of the rfr model under the registered model name
    for run_id in [run1.info.run_id, run2.info.run_id]:
        model_uri = "runs:/{}/sklearn-model".format(run_id)
        mv = client.create_model_version(name, model_uri, run_id)
        print("model version {} created".format(mv.version))
    print("--")

    # Fetch the last version; this will be version 2
    mv = client.get_model_version(name, mv.version)
    print_model_version_info(mv)
