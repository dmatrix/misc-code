import joblib
import mlflow
from mlflow.tracking import MlflowClient

if __name__ == '__main__':
   with open('test.file', 'wb') as f:
      test = range(20)
      joblib.dump(test, f)
   mlflow.set_tracking_uri("http://127.0.0.1:5000")
   exp_info = MlflowClient().get_experiment_by_name("issue_3114")
   exp_id = exp_info.experiment_id if exp_info else MlflowClient().create_experiment("issue_3114")
   with mlflow.start_run(experiment_id=exp_id) as run:
      run_id = run.run_id = run.info.run_uuid

      params = {"n_estimators": 3, "random_state": 0}
      mlflow.log_params(params)
      mlflow.log_artifact('test.file')

      print(f"artifact_uri={mlflow.get_artifact_uri()}")
      print(f"run_id={run_id}")
