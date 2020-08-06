from random import random
import joblib

import mlflow

from mlflow.tracking import MlflowClient

def get_exp_id(name, registry_uri, artifact_location):

   clnt = MlflowClient(registry_uri=registry_uri)
   exp_info = clnt.get_experiment_by_name(name)
   exp_id = exp_info.experiment_id if exp_info else clnt.create_experiment(name, artifact_location=artifact_location)
   return exp_id

if __name__ == '__main__':
   with open('test.file', 'wb') as f:
      test = range(10)
      joblib.dump(test, f)

   local_registry_a = "sqlite:///mlruns_a.db"
   exp_a_uri = "file:///tmp/exp_A"
   mlflow.tracking.set_registry_uri(local_registry_a)
   mlflow.set_tracking_uri(local_registry_a)
   exp_a_id = get_exp_id("experiment_A",local_registry_a, exp_a_uri)
   print(f"Running local model registry={local_registry_a} and experiment_id={exp_a_id}")

   for i in range(3):
      with mlflow.start_run(experiment_id=exp_a_id):
         mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
         mlflow.log_artifact('test.file')
         print(f"artifact_uri={mlflow.get_artifact_uri()}")
   print("-" * 75)
   #
   # Experiment B and different registry
   #

   local_registry_b = "sqlite:///mlruns_b.db"
   exp_b_uri = "file:///tmp/exp_B"
   mlflow.tracking.set_registry_uri(local_registry_b)
   mlflow.set_tracking_uri(local_registry_b)
   exp_b_id = get_exp_id("experiment_B",local_registry_b, exp_b_uri)
   print(f"Running local model registry={local_registry_b} and experiment_id={exp_b_id}")

   for i in range(3):
       with mlflow.start_run(experiment_id=exp_b_id):
           mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
           mlflow.log_artifact('test.file')
           print(f"artifact_uri={mlflow.get_artifact_uri()}")

