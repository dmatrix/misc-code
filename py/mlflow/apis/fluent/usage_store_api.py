from random import random, randint
from pprint import pprint
import warnings

import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Define some tags and feature columns
    tags = {"engineering": "ML Platform",
            "release.candidate": "RC1",
            "release.version": "2.2.0"}
    features = "rooms, zipcode, median_price, school_rating, transport"

    # Create a feature file
    with open("features.txt", 'w') as f:
        f.write(features)

    local_store_uri = "sqlite:///api_mlruns.db"
    mlflow.set_tracking_uri(local_store_uri)

    # Start an run and log entities
    with mlflow.start_run(run_name="My Runs") as run:
        params = {"n_estimators": 3, "random_state": 42}
        sk_learn_rfr = RandomForestRegressor(params)

        # Log params using the MLflow entities
        mlflow.log_params(params)
        mlflow.log_param("num_users", randint(0, 100))
        mlflow.log_metric("keystrokes", random())
        mlflow.log_metric("click_rate", random() + 1)
        mlflow.set_tags(tags)

        # Log model
        mlflow.sklearn.log_model(sk_learn_rfr, artifact_path="sklearn-model")

        # Log artifact
        mlflow.log_artifact("features.txt", artifact_path="features")

        print("run_id: {}".format(run.info.run_id))

        data = mlflow.get_run(mlflow.active_run().info.run_id).data
        tags = {k: v for k, v in data.tags.items() if k.startswith("mlflow.source.")}
        pprint(tags)
