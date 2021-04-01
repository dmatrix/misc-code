import mlflow.pyfunc
import pandas as pd


class MultNum(mlflow.pyfunc.PythonModel):
   def __init__(self, num):
      self._num = num

   def predict(self, context, model_input):
      return model_input.apply(lambda column: column * self._num)


if __name__ == "__main__":
   model_path = "pyfunc_models"
   add5_model = MultNum(5)

   # Log the pyfunc model
   with mlflow.start_run(run_name="Log PyFunc") as run:
      mlflow.pyfunc.log_model(model_path, python_model=add5_model)

      # load back the model
      model_uri = f"runs:/{run.info.run_uuid}/{model_path}"
      loaded_model = mlflow.pyfunc.load_model(model_uri)

      # Use inference to predict output from the model
      model_input = pd.DataFrame([range(10)])
      model_output = loaded_model.predict(model_input)
      assert model_output.equals(pd.DataFrame([range(5, 15)]))
      print(model_output.head())

