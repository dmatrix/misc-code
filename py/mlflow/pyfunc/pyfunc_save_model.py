import mlflow.pyfunc
import pandas as pd

class AddNum(mlflow.pyfunc.PythonModel):
   def __init__(self, num):
      self._num = num

   def predict(self, context, model_input):
      return model_input.apply(lambda column: column + self._num)

if __name__ == "__main__":
   model_path = "add_num_model"
   add5_model = AddNum(5)
   # Save model
   with mlflow.start_run(run_name="Save PyFunc"):
      mlflow.pyfunc.save_model(path=model_path, python_model=add5_model)
   # load back the model
   loaded_model = mlflow.pyfunc.load_model(model_path)

   # # Use inference to predict output from the model
   model_input = pd.DataFrame([range(10)])
   model_output = loaded_model.predict(model_input)
   assert model_output.equals(pd.DataFrame([range(5, 15)]))

