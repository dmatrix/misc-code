import mlflow.xgboost
import xgboost as xgb

if __name__ == '__main__':
   print(mlflow.__version__)

   with mlflow.start_run() as run:
      run_id = run.run_id = run.info.run_uuid


      # read in data
      dtrain = xgb.DMatrix('https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train')
      dtest = xgb.DMatrix('https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test')
      # specify parameters via map
      param = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
      num_round = 2
      bst = xgb.train(param, dtrain, num_round)
      # make prediction
      preds = bst.predict(dtest)
      mlflow.xgboost.autolog()
      print(f"artifact_uri={mlflow.get_artifact_uri()}")
      print(f"run_id={run_id}")
