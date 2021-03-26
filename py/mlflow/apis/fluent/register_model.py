#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#register_model_uri
#
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor


if __name__ == "__main__":
    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    params = {"n_estimators": 3, "random_state": 42}
    # Log MLflow entities
    with mlflow.start_run() as run:
        rfr = RandomForestRegressor(**params).fit([[0, 1]], [1])
        mlflow.log_params(params)
        mlflow.sklearn.log_model(rfr, artifact_path="sklearn-model")

    # Register the model
    model_uri = "runs:/{}/sklearn-model".format(run.info.run_id)
    mv = mlflow.register_model(model_uri, "RandomForestRegressionModel")
    print("Name: {}".format(mv.name))
    print("Version: {}".format(mv.version))

