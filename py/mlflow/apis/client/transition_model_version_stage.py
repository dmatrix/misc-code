import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":

    def print_model_version_info(mv):
        print("Name: {}".format(mv.name))
        print("Version: {}".format(mv.version))
        print("Description: {}".format(mv.description))
        print("Stage: {}".format(mv.current_stage))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    params = {"n_estimators": 3, "random_state": 42}
    name = "RandomForestRegression"
    desc = "A new version of the model using ensemble trees"
    rfr = RandomForestRegressor(**params)

    # Log MLflow entities
    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    # Register model name in the model registry
    client = MlflowClient()
    client.create_registered_model(name)

    # Create a new version of the rfr model under the registered model name
    model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
    mv = client.create_model_version(name, model_uri, run.info.run_id, description=desc)
    print_model_version_info(mv)
    print("--")

    # transition model version from None -> staging
    mv = client.transition_model_version_stage(name, int(mv.version), "staging")
    print_model_version_info(mv)
