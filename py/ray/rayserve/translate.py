import ray
from ray import serve
from transformers import pipeline
import requests

TWEETS = ["Tonight on my walk, I got mad because mom wouldn't let me play with this dog. We stared at each other...he never blinked!",
          "Sometimes. when i am bored. i will stare at nothing. and try to convince the human. that there is a ghost",
          "You little dog shit, you peed and pooed on my new carpet. Bad dog!",
          "I would completely believe you. Dogs and little children - very innocent and open to seeing such things",
          "You've got too much time on your paws. Go check on the skittle. under the, fridge",
          "You sneaky little devil, I can't live without you!!!",
          "It's true what they say about dogs: they are you BEST BUDDY, no matter what!",
          "This dog is way dope, just can't enough of her",
          "This dog is way cool, just can't enough of her",
          "Is a dog really the best pet?",
          "Cats are better than dogs",
          "Totally dissastified with the dog. Worst dog ever",
          "Brilliant dog! Reads my moods like a book. Senses my moods and reacts. What a companinon!"
          ]

def fetch_tweet_text(i):
    text = TWEETS[i]
    return text


@serve.deployment
class Translator:
    def __init__(self):
        # Load model
        self.model = pipeline("translation_en_to_fr", model="t5-small")

    def translate(self, text: str) -> str:
        # Run inference
        model_output = self.model(text)

        # Post-process output to return only the translation text
        translation = model_output[0]["translation_text"]

        return translation

    async def __call__(self, http_request) -> str:
        english_text: str = await http_request.json()
        return self.translate(english_text)

@serve.deployment
class Sentimentor:
    def __init__(self):
        self.model = pipeline(model="roberta-large-mnli")

    def sentiment(self, text):
        result = self.model(text)
        
        return f"label: {result[0]['label']}; score: {result[0]['score']}"

# A composed class is deployed with both sentiment analysis and translations models' classnodes initialized in the constructor
@serve.deployment(route_prefix="/composed", num_replicas=2)
class ComposedModel:
    def __init__(self, translate, sentiment):
        # fetch and initialize deployment handles
        self.translate_model = translate
        self.sentiment_model = sentiment

    async def __call__(self, http_request):
        data = await http_request.json()
        sentiment_ref =  await self.sentiment_model.sentiment.remote(data)
        trans_text_ref = await self.translate_model.translate.remote(data)
        sentiment_val = ray.get(sentiment_ref)
        trans_text = ray.get(trans_text_ref)

        return {'Sentiment': sentiment_val, 'Translated Text': trans_text}


if __name__ == "__main__":
    translate_cls_node = Translator.bind()
    sentiment_cls_node = Sentimentor.bind()
    compose_cls_node = ComposedModel.bind(translate_cls_node, sentiment_cls_node)

    serve.run(compose_cls_node)

    for i in range(len(TWEETS)):
        tweet = fetch_tweet_text(i)
        response = requests.post("http://127.0.0.1:8000/composed", json=tweet)
        print(f"tweet request... : {tweet}")
        print(f"tweet response:{response.text}")
