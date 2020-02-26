# mlflow-tests

Some simple tests to check API usage for the OSS documentation

[experiment_local_store.py](py/mlflow/experiment_local_store.py) creates:
 * creates a model
 * logs the model
 * lists all registered models
 * searches and lists versions of the a registered model
 
 [log_reg_model.py](py/mlflow/log_reg_model.py)
  * creates a model
  * logs the model
  * registers the model with a run_id, which create a new version of loggeed model
  * create a new version of the model with run_id
  * searches and lists versions of the a registered model
  
  [log_create_model.py](py/mlflow/log_create_model.py)
  * creates a model
  * logs the model
  * attempts to register a model, which will fail
  * searches and lists versions of the a registered model
  
  [del_model.py](py/mlflow/del_model.py)
  * takes a version of the model and deletes it
  * searches and lists versions of the a registered model 
  
  [del_all_reg_models.py](py/mlflow/del_all_reg_models.py)
  * deletes all versions of a registered model
  
  [archive_model_versions.py](py/mlflow/archive_model_versions.py)
  * takes a list model's versions and archives them
  * searches and lists versions of the a registered model; their stage should
  indicate as "Archived."

