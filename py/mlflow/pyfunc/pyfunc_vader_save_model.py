import pandas as pd

import mlflow.pyfunc
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


def score_model(model):
    # Use inference to predict output from the customized PyFunc model
    for i, text in enumerate(INPUT_TEXTS):
        text = INPUT_TEXTS[i]['text']
        m_input = pd.DataFrame([text])
        scores = loaded_model.predict(m_input)
        print(f"<{text}> -- {str(scores[0])}")

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
    vader_model = SocialMediaAnalyserModel()

    # Set the tracking URI to use local SQLAlchemy db file and start the run
    # Log MLflow entities and save the model
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    with mlflow.start_run(run_name="Vader Sentiment Analysis") as run:
        model_path = f"{model_path}-{run.info.run_uuid}"
        mlflow.log_param("algorithm", "VADER")
        mlflow.log_param("total_sentiments", len(INPUT_TEXTS))
        mlflow.pyfunc.save_model(path=model_path, python_model=vader_model)

    # load back the saved model, log and register into the model registry
    loaded_model = mlflow.pyfunc.load_model(model_path)
    with mlflow.start_run():
       mlflow.pyfunc.log_model(artifact_path=model_path, python_model=vader_model, registered_model_name=reg_model_name)

    # Load the model from the model registry and score
    model_uri = f"models:/{reg_model_name}/1"
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    score_model(loaded_model)



