import numpy as np
import sklearn.linear_model
import mlflow
from mlflow.models.signature import infer_signature

if __name__ == '__main__':
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    # prepare training data
    X = np.array([[1, 1, 3], [1, 2, 4], [2, 2, 5], [2, 3, 6]])
    y = np.dot(X, np.array([1, 2, 2])) + 3
    # train a model
    with mlflow.start_run() as run:
        reg = sklearn.linear_model.LinearRegression().fit(X, y)
        signature = infer_signature(X, y)
        mlflow.sklearn.log_model(reg, "sk_learn",registered_model_name="SKLearnModel", signature=signature)
