import mlflow

"""
Scenario 2: No tracking server, but an SQLAlchemy compatible backend store.

1. LocalArtifactRepository is used directly via the client to store artifacts
2. SQLAlchemy compatible backend store is used to store MLflow entities.
3. No REST calls; clients interact directly via the APIs through an instance
 of LocalArtifactRepository and an instance SqlAlchemyStore backend store.

Interaction and Flow:

1. MLflowClient APIs --> creates an instance of LocalArtifactRepository (to store artifacts)
2. MLflowClient APIs --> creates an instance of SQLAlchemyStore (to store MLflow entities,
   written to sqlite file mlruns.db)

To launch the UI, use `mlfow ui --backend-store-uri sqlite:///mlruns.db`

Then connect to http://127.0.0.1:5000 in the browser to view the UI
"""
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")
