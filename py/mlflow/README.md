# mlflow-tests

Some simple tests to check API usage for the OSS documentation

[experiment_local_store.py](py/mlflow/experiment_local_store.py) creates:
 * creates a model
 * logs the model
 * lists all registered models
 * lists a version of the a registered model
 
 [log_reg_model.py](py/mlflow/log_reg_model.py)
  * creates a model
  * logs the model
  * registers the model with a run_id, which create a new version of loggeed model
  * create a new version of the model with run_id
  * searches all model version and lists them
  
  [log_create_model.py](py/mlflow/log_create_model.py)
  * creates a model
  * logs the model
  * attempts to register a model, which will fail
  * searches all model version and lists them

 

