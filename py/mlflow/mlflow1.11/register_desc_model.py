import numpy as np
import sklearn.linear_model
import mlflow
from mlflow.models.signature import infer_signature

if __name__ == '__main__':
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    # prepare training data
    X = np.array([[1, 1, 2], [1, 2, 3], [2, 2, 4], [2, 3, 5]])
    y = np.dot(X, np.array([1, 2, 1])) + 3

    # Train a model
    with mlflow.start_run() as run:
        reg = sklearn.linear_model.LinearRegression().fit(X,y)
        score = reg.score(X,y)
        signature = infer_signature(X, y)
        mlflow.log_metric("score", score)
        mlflow.sklearn.log_model(reg, "sk_learn",registered_model_name="SKLearnModel", signature=signature)
