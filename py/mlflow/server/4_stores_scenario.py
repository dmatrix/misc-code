import mlflow

"""
Scenario 4: Tracking server launched at a remote host along with an artifact location and an SQLAlchemy compatible backend store.
This scenarios can have two cases:

Case 1. Launch mlflow server as: mlflow server --backend-store-uri sqlite:///my_mlruns.db -h hostname 
--default-artifact-root {file:/tmp/my_artifacts, s3, sftb, gc, wasb, dbfs, hdfs...}

1. Backend store is at local sqlite:///my_mlruns.db
2. Uri scheme based concrete class of ArtifactStore, e.g., file:/tmp/my_artifacts, s3:/bucket_name, etc.

Artifacts: 
part 1: MLflow Client APIs --> RestStore --> REST Request API Call --> Tracking Server (fetch artifact store URI)
part 2: Tracking Server --> REST Response Response with artifact store URI --> MLflow Client
part 3: MLflowClient --> instance of [scheme]ArtifactStore --> S3/ftp/wasb/gc etc(store artifacts)

MLflow Entities:
part 1: MLflow Client --> instance of SQLAlchemyStore (for MLflow entities, params, runs, metrics, etc)

Case 2:
mlflow server --backend-store-uri postgresql://URI --default-artifact-root s3:/bucket_name -h hostname

1. Backend store is at SQL server at postresql://URI
2. Uri scheme based concrete class of S3ArtifactStore, e.g., s3:/bucket_name, etc.

Artifacts: 
part 1: MLflow Client APIs --> RestStore --> REST Request API Call --> Tracking Server (fetch artifact store URI)
part 2: Tracking Server --> REST Response Response with artifact store URI --> MLflow Client
part 3: MLflowClient --> instance of S3ArtifactStore --> S3(store artifacts)

MLflow Entities:
part 1: MLflow Client APIs --> RestStore --> REST Request API Call --> Tracking Server --> instance of SQLAlchemyStore (for MLflow entities, params, runs, metrics, etc)

This will use the LocalArtifactFileStore (file:/tmp/my_artifacts) for saving artifacts and 
backend SQLAlchemyStore (sqlite:///my_mlruns.db) for saving MLflow entities (runs, params, metrics, tags, etc).

There will be REST calls to port 5000 where the Tracking Service is running.

Run tcpdump -Xlv -i lo0 -vv dst port 5000

You can connect to http://hostname:5000 in the browser to view the UI
"""
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)
    mlflow.set_tracking_uri("http://hostname:5000")
    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")
