import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

if __name__ == "__main__":
    print(mlflow.__version__)
    rf = RandomForestClassifier()
    mlflow.set_registry_uri('/tmp/mlflow')
    with mlflow.start_run() as run:
        mlflow.sklearn.log_model(rf, "sk_model")
        mlflow.log_metric("m1", 2.0)
        mlflow.log_param("p1", "mlflow-slack-question")

