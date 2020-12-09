import mlflow
"""
Scenario 1: No tracking server is involved here, hence no REST APIs. The client directly
interfaces using the APIs with the FileStore. This store is used both for artifact store
and backend stores under the ./mlruns directory

You can then launch the UI with mlflow ui from the same directory where ./mlruns resides.

Client APIs --> FileStore
"""
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)

    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")

