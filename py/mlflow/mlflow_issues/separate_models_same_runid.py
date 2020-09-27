
import mlflow
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LogisticRegression, LinearRegression

if __name__ == "__main__":

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()
    client.create_registered_model("RegressionModels")

    # Create two models under a same run
    m = LinearRegression()
    m2 = LogisticRegression()
    with mlflow.start_run() as run:
        mlflow.log_metric("m", 2.3)
        mlflow.sklearn.log_model(m, "sk_learn_m")

        mlflow.log_metric("m2", 2.5)
        mlflow.sklearn.log_model(m2, "sk_learn_m2")

        # Register different versions in the register under the same run

        mlflow.register_model("runs:/{}/sk_learn_m".format(run.info.run_id), "RegressionModels")
        mlflow.register_model("runs:/{}/sk_learn_m2".format(run.info.run_id), "RegressionModels")
