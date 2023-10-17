import pandas as pd
import datasets

from pprint import pprint
from transformers import AutoTokenizer

# Load the tokenizer for the pythia model
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")
text = "Hi Jules, how are you?"
# tokenize the text
tokenized_text = tokenizer(text)
print(tokenized_text)
print("-----" * 10)

# tokenize a list of text with padding
texts = [text, "Having a go with toknizers", "Fun stuff", "yeah"]
tokenizer.pad_token = tokenizer.eos_token
tokenized_texts = tokenizer(texts, padding=True)
print(tokenized_texts)

# let do truncating and padding together with
max_length = max([len(t) for t in texts])
tokenized_texts = tokenizer(texts, padding=True)
print(tokenized_texts)
print("-----" * 10)

# examing an instructution data set
taylor_swift_dataset = "lamini/taylor_swift"

dataset_swiftie = datasets.load_dataset(taylor_swift_dataset)
print(dataset_swiftie["train"][1])