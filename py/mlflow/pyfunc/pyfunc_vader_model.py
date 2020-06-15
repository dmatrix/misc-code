from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import mlflow.pyfunc

INPUT_TEXTS = [{'text': "This is a bad ass movie. You got to see it! :-)"},
               {'text': "Ricky Gervais is smart, witty, and creative!!!!!! :D"},
               {'text': "LOL, this guy fell off a chair while snoring in a meeting"},
               {'text': "Men shoots himself while trying to steal a dog, OMG"},
               {'text': "Yay!! Another good phone interview!!"},
               {'text': "This is INSANE! I can't believe it. How could you do such a horrible thing?"}]

class SocialMediaAnalyserModel(mlflow.pyfunc.PythonModel):

   def __init__(self):
      self._analyser = SentimentIntensityAnalyzer()

   def _score(self, text):
      scores = self._analyser.polarity_scores(text)
      return scores

   def predict(self, context, model_input):
      model_output = model_input.apply(lambda col: self._score(col))
      return model_output


if __name__ == "__main__":
   model_path = "vader"
   vader_model = SocialMediaAnalyserModel()
   with mlflow.start_run(run_name="Vader Sentiment Analysis") as run:
      mlflow.pyfunc.log_model(model_path, python_model=vader_model)

      # load back the model
      model_uri = f"runs:/{run.info.run_uuid}/{model_path}"
      loaded_model = mlflow.pyfunc.load_model(model_uri)
      mlflow.log_param("algorithm", "VADER")
      mlflow.log_param("total_sentiments", len(INPUT_TEXTS))

      # Use inference to predict output from the model
      for i in range(len(INPUT_TEXTS)):
         text = INPUT_TEXTS[i]['text']
         mlflow.log_param(f"text_{i}", text)
         model_input = pd.DataFrame([text])
         scores = loaded_model.predict(model_input)
         print(f"{text} -------------- {str(scores[0])}")
         for index, value in scores.items():
            [mlflow.log_metric(f"{key}_{i}", value) for key, value in value.items()]
