import mlflow
import joblib

if __name__ == "__main__":
    with open('test.file', 'wb') as f:
        test = range(20)
        joblib.dump(test, f)

    mlflow.set_tracking_uri("http://0.0.0.0:5000")
    with mlflow.start_run() as run:
        run_id = run.info.run_uuid
        mlflow.log_artifact('test.file')
        print(f"artifact_uri: {mlflow.get_artifact_uri()}")
        print(f"run_id: {run_id}")
