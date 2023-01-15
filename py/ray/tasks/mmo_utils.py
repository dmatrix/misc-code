from typing import  Dict, List, Tuple, Any
import time
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import mmd_utils as mmt


from pyarrow import parquet as pq
import pyarrow.compute as pc
import ray

# Redefine the train_and_evaluate task to use in-memory data.
# We still keep file_name and pickup_location_id for identification purposes.
@ray.remote
def train_and_evaluate_optimized(
    pickup_location_id_and_data: Tuple[int, pd.DataFrame],
    file_name: str,
    models: List[BaseEstimator],
    verbose: bool = False,
) -> Tuple[str, str, List[Tuple[BaseEstimator, float]]]:
    """
    An optimized version of this function that uses in-memory data.

    Args:
        pickup_location_id_and_data: A tuple of id and its respective Pandas
        DataFrame
        file_name: file used to extract id's dataframe
        models: list of sklearn estimators to train on
        verbose: boolean, default False to print stats and times
    
    Returns:
        A tuple file_name, id, and list tuple of estimators and respective MAE
    """
    # Extract respective id and data
    pickup_location_id, data = pickup_location_id_and_data

    # Perform transformation
    start_time = time.time()
    # The underlying numpy arrays are stored in the Ray object
    # store for efficient access, making them immutable. We therefore
    # copy the DataFrame to obtain a mutable copy we can transform.
    data = data.copy()
    data = mmt.transform_batch(data)
    transform_time = time.time() - start_time
    if verbose:
        mmt.print_time_info_stats(
            f"Data transform time for LocID: {pickup_location_id}: {transform_time}"
    )

    return (
        file_name,
        pickup_location_id,
        mmt.train_and_evaluate_internal(data, models, pickup_location_id),
    )


@ray.remote(num_returns="dynamic")
def read_into_object_store(file: str) -> ray.ObjectRefGenerator:
    """
    This function creates a Ray Task that is a generator, returning an
    object references. Read the table from the file. It stores the data
    into the Ray object store. 

    Args: 
        str path to the file name

    Returns:
        Yields Ray Object references as tuple of pickup_id and associated data
    """
    # print(f"Loading {file} into arrow table")
    # Read the entire single file into memory.
    try:
        locdf = pq.read_table(
            file,
            columns=[
                "pickup_at",
                "dropoff_at",
                "pickup_location_id",
                "dropoff_location_id",
            ],
        )
        # print(f"Size of pyarrow table: {locdf.shape}")
    except Exception:
        return []

    pickup_location_ids = locdf["pickup_location_id"].unique()

    for pickup_location_id in pickup_location_ids:
        # Each id-data batch tuple will be put as a separate object into the Ray object store.
        # Cast PyArrow scalar to Python if needed.
        try:
            pickup_location_id = pickup_location_id.as_py()
        except Exception:
            pass

        yield (
            pickup_location_id,
            locdf.filter(
                pc.equal(locdf["pickup_location_id"], pickup_location_id)
            ).to_pandas(),
        )

def run_batch_training_with_object_store(
    files: List[str], models: List[BaseEstimator], verbose: bool=False) -> \
            Tuple[Tuple[str, str, List[Tuple[BaseEstimator, float]]], Dict[Any, Any]]:
    """
    An optimized verion of this function that uses scheduling
    strategy and fetches id-data from Ray's object store

    Args:
        List of parquet files to the data
        List of model estimators to use to train

    Returns:
        the results from all the runs and timiings
    """

    print("Starting optimized run: each task fetching pre-loaded data from Ray object store...")
    start = time.time()

    # Store task references
    task_refs = []

    # Use a SPREAD scheduling strategy to load each
    # file on a separate node as an OOM safeguard.
    # This is not foolproof though! We can also specify a resource
    # requirement for memory, if we know what is the maximum
    # memory requirement for a single file.
    read_into_object_store_spread = read_into_object_store.options(
        scheduling_strategy="SPREAD"
    )

    # Dictionary of references to read tasks with file names as keys
    read_tasks_by_file = {
        files[file_id]: read_into_object_store_spread.remote(file)
        for file_id, file in enumerate(files)
    }

    for file, read_task_ref in read_tasks_by_file.items():
        # We iterate over references and pass them to the tasks directly
        for pickup_location_id_and_data_batch_ref in iter(ray.get(read_task_ref)):
            task_refs.append(
                train_and_evaluate_optimized.remote(
                    pickup_location_id_and_data_batch_ref, file, models, verbose=verbose)
                )

    # Block to obtain results from each task
    results = ray.get(task_refs)

    taken = time.time() - start
    count = len(results)
    # If result is None, then it means there weren't enough records to train
    results_not_none = [x for x in results if x is not None]
    count_not_none = len(results_not_none)

    # Sleep a moment for nicer output
    times_stats = {}
    times_stats["total_pickup_locations"] =  count
    times_stats["total_pickup_locations_trained"] =  count_not_none
    times_stats["total_models_trained"] =  count_not_none * len(models)
    times_stats["total_training_time"] =  round(taken, 3)

    return results, times_stats