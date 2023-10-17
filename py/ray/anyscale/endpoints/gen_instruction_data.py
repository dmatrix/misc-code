import random
import jsonlines
import datasets
from datasets import load_dataset
from pprint import pprint



from pprint import pprint
from transformers import AutoTokenizer

def tokenize_function(examples):
    if "question" in examples and "answer" in examples:
      text = examples["question"][0] + examples["answer"][0]
    elif "input" in examples and "output" in examples:
      text = examples["input"][0] + examples["output"][0]
    else:
      text = examples["text"][0]

    tokenizer.pad_token = tokenizer.eos_token
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        padding=True,
    )

    max_length = min(
        tokenized_inputs["input_ids"].shape[1],
        2048
    )
    tokenizer.truncation_side = "left"
    tokenized_inputs = tokenizer(
        text,
        return_tensors="np",
        truncation=True,
        max_length=max_length
    )

    return tokenized_inputs

# List of example questions and answers
questions = [
    "What is the capital of France?",
    "How does photosynthesis work?",
    "Who wrote the play 'Romeo and Juliet'?",
    "What is the boiling point of water?",
    "What is the largest planet in our solar system?",
    "How do vaccines work?",
    "Who painted the Mona Lisa?",
    "What is the process of digestion in the human body?",
    "What is the purpose of the circulatory system?"
    # Add more questions...
]

answers = [
    "The capital of France is Paris.",
    "Photosynthesis is a process by which plants convert sunlight, water, and carbon dioxide into energy, producing oxygen as a byproduct.",
    "'Romeo and Juliet' was written by William Shakespeare.",
    "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit) at standard atmospheric pressure.",
    "The largest planet in our solar system is Jupiter.",
    "Vaccines stimulate the immune system to produce an immune response without causing the disease, providing immunity against future infections.",
    "The Mona Lisa was painted by Leonardo da Vinci.",
    "Digestion is the process by which the body breaks down food into smaller nutrients that can be absorbed and used for energy.",
    "The circulatory system transports oxygen, nutrients, and waste products throughout the body, ensuring proper functioning of organs and tissues."


    # Add more answers...
]

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-70m")

# Generate 10random pairs
training_data = []
for _ in range(10):
    random_index = random.randint(0, len(questions) - 1)
    question = questions[random_index]
    answer = answers[random_index]
    training_data.append({"question": question, "answer": answer})

print("-----" * 10)

prompt_template = """### Question:
{question}

### Answer: """

num_examples = len(training_data)

finetuning_dataset = []
for i in range(num_examples):
  question = training_data[i]["question"]
  answer = training_data[i]["answer"]
  text_with_prompt_template = prompt_template.format(question=question)
  finetuning_dataset.append({"question": text_with_prompt_template, "answer": answer})

print("One datapoint in the finetuning dataset:")
pprint(finetuning_dataset[0])

# save the train_data
filename=f"./random_processed.jsonl"
with jsonlines.open(filename, 'w') as writer:
    writer.write_all(finetuning_dataset)

# load the file back in 
finetuning_dataset_loaded = datasets.load_dataset("json", data_files=filename, split="train")

# let's tokenize the training set

tokenized_dataset = finetuning_dataset_loaded.map(
    tokenize_function,
    batched=True,
    batch_size=1,
    drop_last_batch=True
)
tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])
split_dataset = tokenized_dataset.train_test_split(test_size=0.1, shuffle=True, seed=123)
print(split_dataset)

# processing a HF dataset
def to_upper(example):
   l = example["answer"].upper()
   return {"answer":l}

def to_print(example):
   print(example["answer"])

idx_ds = split_dataset.map(to_upper)
idx_ds.map(to_print)
