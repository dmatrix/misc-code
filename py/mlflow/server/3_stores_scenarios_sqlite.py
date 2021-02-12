import mlflow
'''
Using sqlite:///<path>/mlruns.db for backend store and /tmp/mlruns for artifact store

mlflow server --backend-store-uri sqlite:////tmp/mlruns.db --default-artifact-root /tmp/mlruns
'''
if __name__ == '__main__':
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open("features.txt", 'w') as f:
        f.write(features)
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    with mlflow.start_run():
        mlflow.log_param("p", 'p')
        mlflow.log_metric("m", 1.5)
        mlflow.log_artifact("features.txt")
