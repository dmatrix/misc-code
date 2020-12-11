import mlflow

"""
Scenario 4: Tracking server launched along with an artifact location and an SQLAlchemy compatible backend store

Launch mlflow server as: mlflow server --backend-store-uri sqlite:///my_mlruns.db 
--default-artifact-root {file:/tmp/my_artifacts, s3, sftb, gc, wasb, dbfs, hdfs...}

1. Backend store is at sqlite:///my_mlruns.db
2. Uri scheme based concrete class of ArtifactStore, e.g., file:/tmp/my_artifacts, s3:/bucket_name, etc.

Artifacts: 
part 1: MLflow Client APIs --> RestStore --> REST API Call --> Tracking Server (fetch artifact store URI)
part 2: Tracking Server --> REST API Response with artifact store URI --> MLflow Client
part 3: MLflowClient --> instance of [scheme]ArtifactStore --> S3/ftp/wasb/gc etc(store artifacts)

MLflow Entities:
part 1: MLflow Client --> SQLAlchemyStore (for MLflow entities, params, runs, metrics, etc)

This will use the LocalArtifactFileStore (file:/tmp/my_artifacts) for saving artifacts and 
backend SQLAlchemyStore (sqlite:///my_mlruns.db) for saving MLflow entities (runs, params, metrics, tags, etc).

There will be REST calls to port 5000 where the Tracking Service is running.

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
