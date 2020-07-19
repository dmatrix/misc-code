import mlflow
from random import random, randint

if __name__ == '__main__':
   local_registry = "sqlite:///mlruns.db"
   print(f"Running local model registry={local_registry}")
   mlflow.set_tracking_uri(local_registry)
   for i in range(3):
      with mlflow.start_run():
         mlflow.log_metric("MEAN SQUARE ERROR", 0.25 * random())
