import mlflow

"""
Scenario 3: Tracking server launched at localhost (default port 5000) : mlflow server --backend-store-uri file://path/mlruns

1. Backend store and Artifact Store both use local file://path/mlruns. That is,  they use the LocalArtifactRepository to save artifacts and FileStore to save MLflow entities (runs, params, metrics, tags, etc).
2. Client will use an instance of RestStore and make REST APIs calls to the tracking server at default port 5000
Interaction and Flow:
MLflow Entities:
part 1a & b: MLflowClient  --> creates an instance of RestStore → REST Log MLflow entities Request API Call --> Tracking Server → instance of FileStore (to save MLflow entities–params, runs, metrics, etc)

Artifacts:
part 2a: MLflowClient → RestStore --> REST Request API Call --> Tracking Server (fetch artifact store URI)
part 2b: Tracking Server --> REST Response with artifact store URI --> MLflowClient
part 3: MLflowClient  --> creates an instance of LocalArtifactRepository (to stores artifacts)

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
