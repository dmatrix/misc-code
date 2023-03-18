import psutil
import timeit

from datasets import load_dataset

data_set_url = "https://the-eye.eu/public/AI/pile_preliminary_components/EuroParliamentProceedings_1996_2011.jsonl.zst"
if __name__ == "__main__":

    data_set = load_dataset("json", data_files=data_set_url, split="train", streaming=True)
    print(f"Dataset contents: {data_set}")
    print(f"Sample data: {next(iter(data_set))}")

    # let's check its size in memory

    # Process.memory_info is expressed in bytes, so convert to megabytes
    print(f"RAM used: {psutil.Process().memory_info().rss / (1024 * 1024):.2f} MB")

    print(f"Number of files in dataset : {data_set.dataset_size}")
    size_gb = data_set.dataset_size / (1024**3)
    print(f"Dataset size (cache file) : {size_gb:.2f} GB")


    code_snippet = """batch_size = 1000

    for idx in range(0, len(data_set), batch_size):
        _ = data_set[idx:idx + batch_size]
    """

    time = timeit.timeit(stmt=code_snippet, number=1, globals=globals())
    print(
        f"Iterated over {len(data_set)} examples (about {size_gb:.1f} GB) in "
        f"{time:.1f}s, i.e. {size_gb/time:.3f} GB/s"
    )