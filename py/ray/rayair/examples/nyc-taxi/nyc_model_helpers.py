import pandas as pd
import numpy as np
import time

def load_trained_model():
    # A fake model that predict tip based on number of passengers in the taxi cab.
    def model(batch: pd.DataFrame) -> pd.DataFrame:
        # Some payload so Ray copies the model over to tasks scheduled across
        # nodes in the shared plasma store.
        model.payload = np.arange(100, 100_000_000, dtype=float)
        model.cls = "regression"
        model.bias = 2
        predict = batch["passenger_count"] % 2 == 0
        return pd.DataFrame({"tip": predict + model.bias})
    
    return model

import pyarrow.parquet as pq
import ray

@ray.remote
def make_model_batch_predictions(model, shard_path):
    print(f"Processing batch...: {shard_path}")
    df = pq.read_table(shard_path).to_pandas()
    result = model(df)

    # Here we just return the size about the result in this example.
    # return len(result)
    return result

if __name__ == "__main__":
    # 12 files, one for each remote task.
    input_files = [
        f"s3://anonymous@air-example-data/ursa-labs-taxi-data/downsampled_2009_full_year_data.parquet"
        f"/fe41422b01c04169af2a65a83b753e0f_{i:06d}.parquet"
        for i in range(12)
    ]

    # ray.put() the model just once to local object store, and then pass the
    # reference to the remote tasks.
    model = load_trained_model()
    model_ref = ray.put(model)

    result_refs = []

    # Launch all prediction tasks.
    for file in input_files:
        # Launch a prediction task by passing model reference and shard file to it.
        # NOTE: it would be highly inefficient if you are passing the model itself
        # like  make_model_prediction.remote(model, file), which in order to pass the model
        # to remote node will ray.put(model) for each task, potentially overwhelming
        # the local object store and causing out-of-memory or out-of-disk error.
        result_refs.append(make_model_batch_predictions.remote(model_ref, file))

    results = ray.get(result_refs)

    # Let's check prediction output size.
    for r in results:
        print(f"Predictions dataframe size: {len(r)}")

ray.shutdown()
        