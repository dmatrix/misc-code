import ray
import numpy as np


@ray.remote
def train(data_shard):
    for batch in data_shard:
        # would process batch here here
        print(f"Train model with batch: {batch}")


if __name__ == '__main__':

    ray.init()

    # create an iterator with 4 shards and batch of 1024
    it = (
        ray.util.iter.from_range(1000000, num_shards=4, repeat=True)
        .batch(1024)
        .for_each(np.array)
    )

    # Do some work
    work = [train.remote(shard) for shard in it.shards()]
    print(ray.get(work))

    ray.util.iter.
