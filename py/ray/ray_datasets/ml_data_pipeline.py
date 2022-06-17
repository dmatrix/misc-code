import os
import random
import warnings
import tempfile
import time

from typing import List

import ray
from ray.data.dataset_pipeline import DatasetPipeline
from ray.data.datasource.datasource import RandomIntRowDatasource

# A typical machine learning ingestion pipeline consists of the following 4 steps:
# 1. Load the training data from external storage;
# 2. Iterate over the data for multiple epochs;
# 3. In each epoch, applying global shuffle to decorrelate the data;
# 4. In each epoch, split the shuffled data into shards, and feed shards
#    to distributed trainers;


def create_shuffle_pipeline(training_data_dir: str,
                            num_epochs: int,
                            num_shards: int) -> List[DatasetPipeline]:
    """
    create_shuffle_pipeline function creates an ingestion pipeline.
    It reads training_data_dir, iterates for
    num_epochs times, where in each epoch it shuffles and splits
    the training data into num_shards.
    """
    lst_pipeline = (ray.data.read_parquet(training_data_dir)
                    .repeat(num_epochs)
                    .random_shuffle_each_window()
                    .split(num_shards, equal=True))
    return lst_pipeline

# Let’s also implement a TrainingWorker which consumes the shuffled data
# from each shard. For simplicity, we will define a Ray Actor that emulates
# training workers. Specifically, it takes:
# one shard of the shuffle pipeline for training;
# iterates over the shard to get a training dataset per epoch; and
# then consumes the dataset by batches;


@ray.remote
class TrainingWorker:
    def __init__(self, rank: int, shard: DatasetPipeline):
        self.rank = rank
        self.shard = shard

    def loss_func(self, batch):
        return random.uniform(0, 1) * batch.size / (1024 * 1000)

    def train(self):
        for epoch, training_dataset in enumerate(self.shard.iter_epochs()):
            # Following code emulates epoch based SGD training.
            print(f"Training... worker: {self.rank}, epoch: {epoch}")
            for i, batch in enumerate(training_dataset.iter_batches()):
                # Your actual training code here.
                loss = self.loss_func(batch)
            print(f"epoch: {epoch}; loss:{loss:.3f}")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"

    NUM_TRAINING_WORKERS = 4
    NUM_EPOCHS = 5
    NUM_COLUMNS = 10
    SIZE_100MiB = 100 * 1024 * 1024

    # create a local ray cluster.
    ray.init()

    def generate_example_files(size_bytes: int) -> str:
        tmpdir = tempfile.mkdtemp()
        ray.data.read_datasource(
            RandomIntRowDatasource(),
            n=size_bytes // 8 // NUM_COLUMNS,
            num_columns=NUM_COLUMNS,
        ).write_parquet(tmpdir)
        return tmpdir


    example_files_dir = generate_example_files(SIZE_100MiB)

    splits = create_shuffle_pipeline(
        example_files_dir, NUM_EPOCHS, NUM_TRAINING_WORKERS
    )

    training_workers = [
        TrainingWorker.remote(rank, shard) for rank, shard in enumerate(splits)
    ]

    # Let's run the e2e pipeline
    start = time.time()
    ray.get([worker.train.remote() for worker in training_workers])
    print(f"total ingestion time: {int(time.time() - start)}s")

