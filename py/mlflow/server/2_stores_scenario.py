import mlflow

"""
Scenario 2: MLflow on the localhost with backend store as an SQLAlchemy compatible database type: sqlite

No tracking server, but use an SQLAlchemy compatible backend store for MLflow entities.  Artifacts are stored locally in the local  ./mlruns directory, and MLflow entities are stored in an sqlite database file mlruns.db

Interaction and Flow:
MLflowClient  --> creates an instance of LocalArtifactRepository (to save artifacts)
MLflowClient --> creates an instance of SQLAlchemyStore (to save MLflow entities) and writes to sqlite file mlruns.db)

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
