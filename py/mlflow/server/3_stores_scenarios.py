import mlflow

"""
Scenario 3: Tracking server launched at localhost (default port 5000)
as: mlflow server --backend-store-uri file:/path/my_mlruns

1. Backend store and Artifact Store both use local URI file:/path/my_mlruns. That is, 
it uses the LocaArtifactRespository to save artifacts and FileStore to save MLflow entities (runs, params, metrics, tags, etc).
2. Client will use an instance of RestStore and make REST APIs calls to the tracking server at port 5000

Interaction and Flow:
Artifacts:
part 1: MLflowClient → creates an instance of RestStore --> REST Request API Call --> Tracking Server (fetch artifact store URI)
part 2: Tracking Server --> REST Response with artifact store URI --> MLflowClient
part 3: MLflowClient --> creates an instance of LocalArtifactRepository (to store artifacts)

MLflow Entities:
part 4: MLflowClient --> creates an instance of FileStore (to store MLflow entities–params, runs, metrics, etc)

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
