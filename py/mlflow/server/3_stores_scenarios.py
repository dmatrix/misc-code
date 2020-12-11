import mlflow

"""
Scenario 3: Tracking server launched at localhost or some host (default port 5000)
as: mlflow server --backend-store-uri file:/Users/julesdamji/examples/py/mlflow/server/my_mlruns

1. Backend store and Artifact Store are both used local FileStore at ./my_runs. That is, it 
uses the FileStore for saving artifacts and MLflow entities (runs, params, metrics, tags, etc).
2. Client will use REST calls to talk to tracking server at port 5000 for the APIs calls

Artifacts: 
part 1: MLflow Client APIs --> RestStore --> REST API Call --> Tracking Server (fetch artifact store URI)
part 2: Tracking Server --> REST API Response with artifact store URI --> MLflow Client
part 3: MLflow Client --> LocalArtifactFileStore (store artifacts)

MLflow Entities:
part 1: MLflow Client --> LocalFileStore (for MLflow entities, params, runs, metrics, etc)

Run tcpdump -Xlv -i lo0 -vv dst port 5000 to see the traffic to port 5000

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
