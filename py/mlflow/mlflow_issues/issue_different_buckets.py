from random import random
import joblib

import mlflow

from mlflow.tracking import MlflowClient

def get_exp_id(name, uri):
   exp_info = MlflowClient().get_experiment_by_name(name)
   exp_id = exp_info.experiment_id if exp_info else MlflowClient().create_experiment(name, artifact_location=uri)
   return exp_id

if __name__ == '__main__':
   with open('test.file', 'wb') as f:
      test = range(10)
      joblib.dump(test, f)

   clt = MlflowClient()
   exp_a_uri = "file:///tmp/exp_A"
   exp_a_id = get_exp_id("experiment_A",exp_a_uri)
   exp_b_uri = "file:///tmp/exp_B"
   exp_b_id = get_exp_id("experiment_B", exp_b_uri)

   for i in range(3):
      with mlflow.start_run(experiment_id=exp_a_id):
         mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
         mlflow.log_artifact('test.file')
         print(f"artifact_uri={mlflow.get_artifact_uri()}")

   for i in range(3):
       with mlflow.start_run(experiment_id=exp_b_id):
           mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
           mlflow.log_artifact('test.file')
           print(f"artifact_uri={mlflow.get_artifact_uri()}")
