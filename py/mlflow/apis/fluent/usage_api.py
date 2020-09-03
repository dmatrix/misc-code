from random import random, randint
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
import warnings

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    tags = {"engineering": "ML Platform",
            "release.candidate": "RC1",
            "release.version": "2.2.0"}

    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    with mlflow.start_run(run_name="My Runs") as run:
        params = {"n_estimators": 3, "random_state": 42}
        sk_learn_rfr = RandomForestRegressor(params)

        # Log params using the MLflow entities
        mlflow.log_params(params)
        mlflow.log_param("param_1", randint(0, 100))
        mlflow.log_metric("metric_1", random())
        mlflow.log_metric("metric_2", random() + 1)
        mlflow.set_tags(tags)

        # Log model
        mlflow.sklearn.log_model(sk_learn_rfr, artifact_path="sklearn-model")

        # Log artifact
        mlflow.log_artifact("features.txt", artifact_path="features")
