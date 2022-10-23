import pandas as pd
import numpy as np
import pyarrow.parquet as pq

import ray
from ray.util.actor_pool import ActorPool

NUM_ACTORS = 5
NUM_SHARD_FILES = 12

def load_trained_model():
    # A fake model that predict tip based on number of passengers in the taxi cab.
    def model(batch: pd.DataFrame) -> pd.DataFrame:
        # Some payload so Ray copies the model over to tasks scheduled across
        # nodes in the shared plasma store.
        model.payload = np.arange(100, 100_000_000, dtype=float)
        model.cls = "regression"
        predict = batch["passenger_count"] >= 2 
        return pd.DataFrame({"score": predict})
    
    return model

@ray.remote
class BatchPredictor:
    def __init__(self, model):
        self.model = model

    def predict(self, shard_path):
        df = pq.read_table(shard_path).to_pandas()
        result = self.model(df)
        return result


if __name__ == "__main__":
    model = load_trained_model()
    model_ref = ray.put(model)

    # create a pool of five actors
    actors = [BatchPredictor.remote(model_ref) for _ in range(NUM_ACTORS)]
    actors_pool = ActorPool(actors)

    # iterate thorough our NYC files
    input_shard_files = [
        f"s3://anonymous@air-example-data/ursa-labs-taxi-data/downsampled_2009_full_year_data.parquet"
        f"/fe41422b01c04169af2a65a83b753e0f_{i:06d}.parquet"
        for i in range(NUM_SHARD_FILES) ]

    for shard_path in input_shard_files:
        # Submit file shard for prediction to the pool
        actors_pool.submit(lambda actor, shard: actor.predict.remote(shard), shard_path)

    while actors_pool.has_next():
        r =  actors_pool.get_next()
        print(f"Predictions dataframe size: {len(r)} | Total score for tips: {r['score'].sum()}")






