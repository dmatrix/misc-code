from transformers import TranslationPipeline, TextClassificationPipeline
from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForSequenceClassification
import torch

TWEETS = ["Tonight on my walk, I got mad because mom wouldn't let me play with this dog. We stared at each other...he never blinked!",
          "Sometimes. when i am bored. i will stare at nothing. and try to convince the human. that there is a ghost",
          "You little dog shit, you peed and pooed on my new carpet. Bad dog!",
          "I would completely believe you. Dogs and little children - very innocent and open to seeing such things",
          "You've got too much time on your paws. Go check on the skittle. under the, fridge",
          "You sneaky little devil, I can't live without you!!!",
          "It's true what they say about dogs: they are you BEST BUDDY, no matter what!"
          "This dog is way dope, just can't enough of her",
          ]

# Step 1: A Python script that translates tweets to French and identify as sentiments
# No Ray Serve yet


# Fetch Tweet
def fetch_tweet_text(i):
    text = TWEETS[i]
    return text


def sentiment_model(text: str):
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, task="sentiment-analysis")

    return pipeline(text)[0]['label'], pipeline(text)[0]['score']


def translate_model(text: str):
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelWithLMHead.from_pretrained("t5-small")
    use_gpu = 0 if torch.cuda.is_available() else -1
    pipeline = TranslationPipeline(model, tokenizer, task="translation_en_to_fr", device=use_gpu)

    return pipeline(text)[0]['translation_text']


def main():
    for i in range(len(TWEETS)):
        tweet_text = fetch_tweet_text(i)
        sentiment, score = sentiment_model(tweet_text)
        translated_text = translate_model(tweet_text)
        print(f'Sentiment: {sentiment}, score: {score:.3f}, Translated Text: {translated_text}')


if __name__ == "__main__":
    main()
