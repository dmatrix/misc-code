from random import random
import joblib

import mlflow

from mlflow.tracking import MlflowClient

def get_exp_id(name, tracking_uri, registry_uri, artifact_uri):
   exp_info = MlflowClient(tracking_uri=tracking_uri, registry_uri=registry_uri).get_experiment_by_name(name)
   exp_id = exp_info.experiment_id if exp_info else MlflowClient().create_experiment(name, artifact_location=artifact_uri)
   return exp_id

if __name__ == '__main__':
   with open('test.file', 'wb') as f:
      test = range(10)
      joblib.dump(test, f)

   local_registry = "sqlite:///mlruns.db"
   print(f"Running local model registry={local_registry}")
   mlflow.set_tracking_uri(local_registry)

   clt = MlflowClient()
   exp_a_uri = "file:///tmp/exp_A"
   exp_a_id = get_exp_id("experiment_A",local_registry, local_registry, exp_a_uri)
   exp_b_uri = "file:///tmp/exp_B"
   exp_b_id = get_exp_id("experiment_B", local_registry, local_registry, exp_b_uri)

   for i in range(3):
      with mlflow.start_run(experiment_id=exp_a_id):
         mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
         mlflow.log_artifact('test.file')
         print(f"artifact_uri={mlflow.get_artifact_uri()}")
   print("-" * 75)
   for i in range(3):
       with mlflow.start_run(experiment_id=exp_b_id):
           mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
           mlflow.log_artifact('test.file')
           print(f"artifact_uri={mlflow.get_artifact_uri()}")
