import warnings

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn import tree
from mlflow.models.signature import infer_signature


def main(name):
   iris = load_iris()
   sk_model = tree.DecisionTreeClassifier()
   sk_model = sk_model.fit(iris.data, iris.target)
   predictions = sk_model.predict(iris.data[0:5])
   signature = infer_signature(iris.data, predictions)

   # Log model params
   mlflow.log_param("criterion", sk_model.criterion)
   mlflow.log_param("splitter", sk_model.splitter)

   # Log model and register the model with signature
   mlflow.sklearn.log_model(sk_model=sk_model,
                            artifact_path="sklearn-cls-model",
                            registered_model_name=name,
                            signature=signature)


if __name__ == '__main__':
   warnings.filterwarnings("ignore")
   print(mlflow.__version__)

   # Set the tracking server to be localhost with sqlite as tracking store
   local_registry = "sqlite:///mlruns.db"
   mlflow.set_tracking_uri(local_registry)
   print(f"Running local model registry={local_registry}")
   model_name = "IrisClassifierModel"
   main(model_name)
