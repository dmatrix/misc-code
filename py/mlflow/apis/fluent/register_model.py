#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#register_model_uri
#
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":

    mlflow.set_tracking_uri("sqlite:////tmp/mlruns.db")
    params = {"n_estimators": 3, "random_state": 42}

    # Log MLflow entities
    with mlflow.start_run(run_name="My Runs") as run:
        rfr = RandomForestRegressor(params)
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
    mv = mlflow.register_model(model_uri, "RandomForestRegressionModel")
    print("Name: {}".format(mv.name))
    print("Version: {}".format(mv.version))

