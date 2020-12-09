import mlflow

"""
Scenario 4: Tracking server launched along with an artifact location and an SQLAlchemy compatible backend store

Launch mlflow server as: 
mlflow server --backend-store-uri sqlite:///my_mlruns.db 
--default-artifact-root file:/tmp/my_artifacts

1. Backend store is at sqlite:///my_mlruns.db
2. FileStore is at file:/tmp/my_artifacts

This will use the FileStore (file:/tmp/my_artifacts) for saving artifacts and 
backend store (sqlite:///my_mlruns.db) for saving MLflow entities (runs, params, metrics, tags, etc).

There will be REST calls to port 5000 where the Tracking Service respectively with the 
FileStore and the SQLAlchemy compatible backend store.

Run tcpdump -Xlv -i lo0 -vv dst port 5000

You can connect to http://127.0.0.1:5000 in the browser to view the UI
"""
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")
