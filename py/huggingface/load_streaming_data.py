from itertools import islice
from datasets import interleave_datasets
from datasets import load_dataset

data_set_url = "https://the-eye.eu/public/AI/pile_preliminary_components/PUBMED_title_abstracts_2019_baseline.jsonl.zst"
if __name__ == "__main__":

    data_set = load_dataset("json", data_files=data_set_url, split="train", streaming=True)
    print(f"Dataset contents: {data_set}")

    print("---" * 5)

    shuffled_dataset = data_set.shuffle(buffer_size=10_000, seed=42)

    dataset_head = shuffled_dataset.take(1)
    dict_data = list(dataset_head)[0]
    print("---" * 5)
    print(f"meta: {dict_data['meta']}")
    print(f"text: {dict_data['text']}")

    # combine two datasets using interleave
    # stream second data set 
    law_dataset_streamed = load_dataset(
    "json",
    data_files="https://the-eye.eu/public/AI/pile_preliminary_components/FreeLaw_Opinions.jsonl.zst",
    split="train",
    streaming=True,
)
    print(next(iter(law_dataset_streamed)))

    # combine the datasets

    combined_dataset = interleave_datasets([data_set, law_dataset_streamed])
    print(list(islice(combined_dataset, 2)))


    


    