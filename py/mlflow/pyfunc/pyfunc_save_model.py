import pandas as pd

import mlflow.pyfunc

def assert_and_score_model(model):
   # Use inference to predict output from the model
   model_input = pd.DataFrame([range(10)])
   model_output = model.predict(model_input)
   assert model_output.equals(pd.DataFrame([range(5, 15)]))


class AddNum(mlflow.pyfunc.PythonModel):
   def __init__(self, num):
      self._num = num

   def predict(self, context, model_input):
      return model_input.apply(lambda column: column + self._num)


if __name__ == "__main__":

   add5_model = AddNum(5)
   reg_model_name = "AddNumPyFunc"

   mlflow.set_tracking_uri("sqlite:///mlruns.db")

   # Save model
   with mlflow.start_run(run_name="Save PyFunc") as run:
      model_path = f"add_num_model-{run.info.run_uuid}"
      mlflow.pyfunc.save_model(path=model_path, python_model=add5_model)

   # load back the model and score
   loaded_model = mlflow.pyfunc.load_model(model_path)
   assert_and_score_model(loaded_model)

   # log and register the model using MLflow API
   with mlflow.start_run():
      mlflow.pyfunc.log_model(artifact_path=model_path, python_model=add5_model, registered_model_name=reg_model_name)

   # load back from the model registry and do the inference
   model_uri = "models:/{}/1".format(reg_model_name)
   loaded_model = mlflow.pyfunc.load_model(model_uri)
   assert_and_score_model(loaded_model)



