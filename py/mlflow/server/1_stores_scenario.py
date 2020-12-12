import mlflow
"""
Scenario 1: No tracking server is involved here, as we run everything localy on our the host,
hence no REST APIs. The MLflowClient directly interfaces with the FileStore. This store is used 
both for artifact store and backend store under the ./mlruns directory.

That is, the artifacts and MLflow entities (runs, params, metrics, tags, etc) are store under
./mlruns local directory. You can then launch the UI with mlflow ui from the same directory where ./mlruns resides.

MlflowClient APIs --> instance LocalArtifactFileStore (store artifacts)
MLflowClient APIs --> instance of FileStore (store MLflow entities)

"""
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")

