import ray
from ray import serve
from regex import D
from send2trash import TrashPermissionError

from transformers import pipeline


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


@serve.deployment
class Summarizer:
    def __init__(self, translator):
        # Load model
        self.model = pipeline("summarization", model="t5-small")
        self.translator = translator

    def summarize(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5, max_length=25)

        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]
        return summary

    async def __call__(self, http_request) -> str:
        english_text: str = await http_request.json()
        summary = self.summarize(english_text)

        translation_ref = await self.translator.translate.remote(summary)
        translation = ray.get(translation_ref)

        return translation


if __name__== "__main__":    
    deployment_graph = Summarizer.bind(Translator.bind())
    serve.run(deployment_graph)

    # send requests
    import requests

    english_text = (
        "It was the best of times, it was the worst of times, it was the age "
        "of wisdom, it was the age of foolishness, it was the epoch of belief"
    )
    response = requests.post("http://127.0.0.1:8000/", json=english_text)
    french_text = response.text
    print(f"English: {english_text}")
    print(f"French:{french_text}")
    print(french_text)