import mlflow
from mlflow.tracking import MlflowClient

if __name__ == '__main__':
   print(mlflow.__version__)

   with mlflow.start_run(run_name='PARENT_RUN',nested=True) as run_parent:
      parent_run_id = run_parent.info.run_id
      mlflow.log_param("parent", "yes")
      with mlflow.start_run(run_name='CHILD_1_RUN', nested=True) as run_child:
         child_run_id = run_child.info.run_id
         mlflow.log_param("child_1", "yes")
         print(f"child_1 runid={child_run_id}")
      with mlflow.start_run(run_name='CHILD_2_RUN',nested=True) as run_child2:
         child2_run_id = run_child2.info.run_id
         print(f"child_2 runid={child2_run_id}")
         mlflow.log_param("child_2", "yes")

   client = MlflowClient()
   query = f"tags.mlflow.parentRunId = '{parent_run_id}'"
   results = client.search_runs(experiment_ids="0",filter_string=query)
   print(results)

   query = "tags.mlflow.runName LIKE '%CHILD%'"
   results = client.search_runs(experiment_ids="0", filter_string=query)
   print(results)

