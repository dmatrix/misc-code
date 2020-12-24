import mlflow

"""
Scenario 4: Tracking server launched at a remote host along with an artifact location and an SQLAlchemy 
compatible backend store. 

mlflow server --backend-store-uri postgresql://URI --default-artifact-root s3:/bucket_name --host hostname

1. Backend store is at SQL server at postresql://URI
2. URI scheme-based concrete class of S3ArtifactRepository for URI s3:/bucket_name

1. Backend store is a PostgreSQL://URI at a remote host
2. URI scheme-based concrete class of S3ArtifactRepository for URI S3:/bucket_name

MLflow Entities:
part 1a & b: MLflowClient --> RestStore --> REST Request API Call --> Tracking Server --> creates an  instance of  SQLAlchemyStore (to store MLflow entities, params, runs, metrics, etc) connects to remote host Postgres DB
Artifacts:
part 2a: MLflowClient --> RestStore --> REST Request API Call --> Tracking Server ( fetch artifact store URI)
part 2b: Tracking Server --> REST Response Response with artifact store URI --> MLflowClient
part 3: MLflowClient --> instance of S3ArtifactRepository --> S3 remote host  bucket (to store artifacts)

The MLflowClient  will use the S3ArtifactRepository (s3:/bucket_name/) to save artifacts on the remote S3 bucket, and the Tracking Server will use an existing instance of SQLAlchemyStore (postresql://URI) to save MLflow entities (runs, params, metrics, tags, etc), after each REST request to log MLflow entities.


There will be REST calls to port 5000 where the Tracking Service is running.

Run tcpdump -Xlv -i lo0 -vv dst port 5000

You can connect to http://hostname:5000 in the browser to view the MLflow UI
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
