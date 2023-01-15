from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from tqdm import tqdm
import mmo_utils as ommt
import matplotlib.pyplot as plt
from pyarrow import dataset as ds
import ray

my_runtime_env = {"working_dir": "."}

if __name__ == "__main__":

    if ray.is_initialized():
        ray.shutdown()
    ray.init(runtime_env=my_runtime_env, ignore_reinit_error=True)

    # Let's read the data as pyarrow table
    dataset = ds.dataset(
        "s3://anonymous@air-example-data/ursa-labs-taxi-data/by_year/",
        partitioning=["year", "month"],
    )
    # Let's use three sklearn estimator models
    models = [LinearRegression(), 
              DecisionTreeRegressor(),
              DecisionTreeRegressor(splitter="random"),
              ]
    all_stats_times = []
    starting_indexes = [-3, -6, -9, -12, -15, -18]
    for starting_idx in tqdm(starting_indexes):
        files = [f"s3://anonymous@{file}" for file in tqdm(dataset.files)][starting_idx:]
        print(f"Total files obtained {len(files)}")
        results, time_stats = ommt.run_batch_training_with_object_store(files, models=models)
        all_stats_times.append(time_stats)
        print(f"Sample of results: {results[:-1][0]}")
        print("", flush=True)
        print(f"Total number of pickup locations: {time_stats['total_pickup_locations']}")
        print(f"Total number of pickup locations with enough records to train: {time_stats['total_pickup_locations_trained']}")
        print(f"Total number of models trained: {time_stats['total_models_trained']}")
        print(f"TOTAL TIME TAKEN: {time_stats['total_training_time']} seconds")
        print("--" * 10)
    
    #  Print all cumulative results and stats
    all_stats_times_df = pd.DataFrame(all_stats_times, index=[3, 6, 9, 12, 15, 18])
    print(all_stats_times_df)

    # Plot some times
    all_stats_times_df.plot(kind="bar")

    plt.ylabel("Total locations, Models Trained, Training times", fontsize=12)
    plt.xlabel("Number of files per batch", fontsize=12)
    plt.title("Optimized batch training with Ray object store")
    plt.grid(False)
    plt.show()