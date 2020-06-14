import mlflow.pyfunc
import pandas as pd

import pytemperature

class ConvertK2F(mlflow.pyfunc.PythonModel):
   def __init__(self):
      self._func = pytemperature.k2f

   def predict(self, context, model_input):
      return model_input.apply(self._func)

if __name__ == "__main__":
   model_path = "pyfunc_models"
   k2f_model = ConvertK2F()
   # Log the pyfunc model
   with mlflow.start_run(run_name="Try PyFunc") as run:
      mlflow.pyfunc.log_model(model_path, python_model=k2f_model)

      # load back the model
      model_uri = f"runs:/{run.info.run_uuid}/{model_path}"
      loaded_model = mlflow.pyfunc.load_model(model_uri)

      # Use inference to predict output from the model
      model_input = pd.DataFrame([range(100, 300, 5)])
      model_output = loaded_model.predict(model_input)
      model_output.rename_axis(['Fahrenheit'], axis=0, inplace=True)
      print(model_output.head())


