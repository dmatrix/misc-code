import pandas as pd

import mlflow.pyfunc
from mlflow.tracking import MlflowClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#
# Good and readable paper from the authors of this package
# http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf

INPUT_TEXTS = [{'text': "This is a bad movie. You don't want to see it! :-)"},
               {'text': "Ricky Gervais is smart, witty, and creative!!!!!! :D"},
               {'text': "LOL, this guy fell off a chair while sleeping and snoring in a meeting"},
               {'text': "Men shoots himself while trying to steal a dog, OMG"},
               {'text': "Yay!! Another good phone interview. I nailed it!!"},
               {'text': "This is INSANE! I can't believe it. How could you do such a horrible thing?"}]


def print_model_version_info(mv):
   print("Name: {}".format(mv.name))
   print("Version: {}".format(mv.version))
   print("Stage: {}".format(mv.current_stage))


class SocialMediaAnalyserModel(mlflow.pyfunc.PythonModel):

   def __init__(self):
      super().__init__()
      self._analyser = SentimentIntensityAnalyzer()

   # preprocess the input with prediction from the vader sentiment model
   def _score(self, txt):
      prediction_scores = self._analyser.polarity_scores(txt)
      return prediction_scores

   def predict(self, context, model_input):

      # Apply the preprocess function from the vader model to score
      model_output = model_input.apply(lambda col: self._score(col))
      return model_output


if __name__ == "__main__":
   model_path = "vader"
   reg_model_name = "PyFuncVaderSentiments"

   # Set the tracking URI to use local SQLAlchemy db file and start the run
   # Log Mlflow entities and register the model
   mlflow.set_tracking_uri("sqlite:///mlruns.db")
   vader_model = SocialMediaAnalyserModel()
   with mlflow.start_run(run_name="Vader Sentiment Analysis"):
      mlflow.log_param("algorithm", "VADER")
      mlflow.log_param("total_sentiments", len(INPUT_TEXTS))
      mlflow.pyfunc.log_model(artifact_path=model_path, python_model=vader_model, registered_model_name=reg_model_name)
   # Load the model from the model registry
   model_uri = f"models:/{reg_model_name}/1"
   loaded_model = mlflow.pyfunc.load_model(model_uri)

   # Use inference to predict output from the customized PyFunc model
   for i, text in enumerate(INPUT_TEXTS):
      text = INPUT_TEXTS[i]['text']
      m_input = pd.DataFrame([text])
      scores = loaded_model.predict(m_input)
      print(f"<{text}> -- {str(scores[0])}")

   # If required, promote the model to staging
   client = MlflowClient()
   versions = client.get_latest_versions(reg_model_name, stages=["Staging"])

   # If not in staging, promote to staging
   print("--")
   if not versions:
      mv = client.transition_model_version_stage(reg_model_name, 1, "Staging")
      print_model_version_info(mv)
   else:
      for version in versions:
         print_model_version_info(version)


