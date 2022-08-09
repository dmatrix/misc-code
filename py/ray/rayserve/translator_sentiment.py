from transformers import TranslationPipeline, TextClassificationPipeline
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForSequenceClassification
import torch
import requests
import ray
from ray import serve

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

# Our class deployment model to analyse the tweet using a pretrained transformer from HuggingFace 🤗.
# Note we have number of `replicas=1` but to scale it, we can increase the number of replicas, as
# we have done below.
@serve.deployment(num_replicas=1)
class SentimentTweet:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.pipeline = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer, task="sentiment-analysis")

    def sentiment(self, text: str):
        return (f"label:{self.pipeline(text)[0]['label']}; score={self.pipeline(text)[0]['score']}")
    
# class to translate a tweet from English --> French 
# using a pretrained Transformer from HuggingFace
@serve.deployment(num_replicas=2)
class TranslateTweet:
    def __init__(self):
         self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
         self.model = AutoModelWithLMHead.from_pretrained("t5-small")
         self.use_gpu = 0 if torch.cuda.is_available() else -1
         self.pipeline = TranslationPipeline(self.model, self.tokenizer, task="translation_en_to_fr", device=self.use_gpu)

    def translate(self, text: str):
        return self.pipeline(text)[0]['translation_text']

# A composed class is deployed with both sentiment analysis and translations models' classnodes initialized in the constructor
@serve.deployment(route_prefix="/composed", num_replicas=2)
class ComposedModel:
    def __init__(self, translate, sentiment):
        # fetch and initialize deployment handles
        self.translate_model = translate
        self.sentiment_model = sentiment

    async def __call__(self, http_request):
        data = await http_request.json()
        sentiment_ref = await self.sentiment_model.sentiment.remote(data)
        trans_text_ref = await self.translate_model.translate.remote(data)
        sentiment_val = ray.get(sentiment_ref)
        trans_text = ray.get(trans_text_ref)

        return {'Sentiment': sentiment_val, 'Translated Text': trans_text}

if __name__ == "__main__":

    translate_cls_node = TranslateTweet.bind()
    sentiment_cls_node = SentimentTweet.bind()
    compose_cls_node = ComposedModel.bind(translate_cls_node,sentiment_cls_node )

    serve.run(compose_cls_node)

    
    for i in range(len(TWEETS)):
        tweet = fetch_tweet_text(i)
        response = requests.post("http://127.0.0.1:8000/composed", json=tweet)
        print(f"tweet request... : {tweet}")
        print(f"tweet response:{response.text}")