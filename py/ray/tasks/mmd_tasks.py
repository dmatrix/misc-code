import os
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from tqdm import tqdm
import mmd_utils as mmt
from pyarrow import dataset as ds
import ray

# Use this flag to test with smaller files for testing & debugging
SMOKE_TEST = True

if __name__ == "__main__":

    if ray.is_initialized():
        ray.shutdown()
    ray.init(ignore_reinit_error=True)

    # Let's read the data as pyarrow table
    dataset = ds.dataset(
        "s3://anonymous@air-example-data/ursa-labs-taxi-data/by_year/",
        partitioning=["year", "month"],
    )
    starting_idx = -1 if SMOKE_TEST else 0
    files = [f"s3://anonymous@{file}" for file in tqdm(dataset.files)][starting_idx:]
    print(f"Total files obtained {len(files)}")

    # Let's use three sklearn estimator models
    models = [LinearRegression(), 
              DecisionTreeRegressor(),
              DecisionTreeRegressor(splitter="random"),
              ]

    results, time_stats = mmt.run_batch_training(files, models=models, verbose=False)
    print(f" Sample of results: {results[:-1][0]}")
    print("", flush=True)
    print(f"Total number of pickup locations: {time_stats['total_pickup_locations']}")
    print(f"Total number of pickup locations with enough records to train: {time_stats['total_pickup_locations_trained']}")
    print(f"Total number of models trained: {time_stats['total_models_trained']}")
    print(f"TOTAL TIME TAKEN: {time_stats['total_training_time']} seconds")
