from typing import  List, Dict, Any, Tuple
import time
import pandas as pd

from sklearn.base import BaseEstimator
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from pyarrow import dataset as ds
from pyarrow import parquet as pq

import ray

def print_time_info_stats(msg: str) -> None:
    print(msg)

def read_data(file: str, pickup_location_id: int) -> pd.DataFrame:
    """
    Read a file into a PyArrow table, convert to pandas and return  
    as Pandas DataFrame. Use push-down predicates since PyArrow
    supports it and only extract the needed fields, filtered
    on pickup_location_id
    Args:
        file: str path to the parquet file containing data
        pickup_location_id: int id to filter out

    Returns:
        Pandas DataFrame filtered by pickup_location_id and respective 
        columns
    """
    return pq.read_table(
        file,
        filters=[("pickup_location_id", "=", pickup_location_id)],
        columns=[
            "pickup_at",
            "dropoff_at",
            "pickup_location_id",
            "dropoff_location_id",
        ],
    ).to_pandas()

def transform_batch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given a Pandas DataFrame as an argument, tranform time format 
    for the pickup and drop times, and return the transformed Pandas
    DataFrame. Having the duration in only seconds helps for easy
    math operations.

    Args:
        df: Pandas DataFrame to be transformed

    Returns:
        a transformed Pandas DataFrame with time formats and duration
        in seconds as an additonal column
    """
    df["pickup_at"] = pd.to_datetime(
        df["pickup_at"], format="%Y-%m-%d %H:%M:%S"
    )
    df["dropoff_at"] = pd.to_datetime(
        df["dropoff_at"], format="%Y-%m-%d %H:%M:%S"
    )
    df["trip_duration"] = (df["dropoff_at"] - df["pickup_at"]).dt.seconds
    df["pickup_location_id"] = df["pickup_location_id"].fillna(-1)
    df["dropoff_location_id"] = df["dropoff_location_id"].fillna(-1)
    return df

@ray.remote
def fit_and_score_sklearn(
    train: pd.DataFrame, test: pd.DataFrame, model: BaseEstimator
) -> Tuple[BaseEstimator, float]:
    """
    A Ray remote task that fits and scores a sklearn model base estimator with the train and test 
    data set supplied. Each Ray task will train on its respective batch of dataframe comprised of
    a pickup_location_id.The model will establish a linear relationship between the dropoff location
    and the trip duration.

    Args:
        train: Pandas DataFrame training data
        test: Pandas DataFrame test data
        model: sklearn BaseEstimator

    Returns: 
        a Tuple of a fitted model and its corrosponding mean absolute error (MAE)
    """
    train_X = train[["dropoff_location_id"]]
    train_y = train["trip_duration"]
    test_X = test[["dropoff_location_id"]]
    test_y = test["trip_duration"]

    # Start training.
    model = model.fit(train_X, train_y)
    pred_y = model.predict(test_X)
    error = round(mean_absolute_error(test_y, pred_y), 3)
    return model, error


def train_and_evaluate_internal(
    df: pd.DataFrame, models: List[BaseEstimator], pickup_location_id: int = 0
) -> List[Tuple[BaseEstimator, float]]:
    """
    A Python functional task which contains all logic necessary to load a data batch, 
    transform it, split it into train and test and fit and evaluate 
    models on it by invoking a remote Ray task. 
    
    Args:
        df: Pandas DataFrame holding transformed data
        models: List of BaseEstimators models to train data on
        pickup_location_id: int location id 

    Returns: 
        The list of fitted models and its corrosponding MAE.
    """
    # We need at least 4 rows to create a train / test split.
    if len(df) < 4:
        # print(f"Dataframe for LocID: {pickup_location_id} is empty or smaller than 4")
        return None

    # Train / test split.
    train, test = train_test_split(df) 

    # We put the train & test dataframes into Ray object store
    # so that they can be reused by all models fitted here.
    # https://docs.ray.io/en/master/ray-core/patterns/pass-large-arg-by-value.html
    # This is the only time in this approach we explicity put data into the 
    # Ray object store.
    train_ref = ray.put(train)
    test_ref = ray.put(test)

    # Launch a fit and score task for each scklearn BaseEstimator model.
    # this will block until all the modesl have been trained.
    results = ray.get(
        [
            fit_and_score_sklearn.remote(train_ref, test_ref, model)
            for model in models
        ]
    )
    # Since we are doing a ray.get above, the results will block.
    # They contain a Tuple of (fitted model, mae), so sort the list of
    # tuples by mae error,in ascending order
    results.sort(key=lambda x: x[1])  # sort by error
    return results

@ray.remote
def train_and_evaluate(
    file_name: str,
    pickup_location_id: int,
    models: List[BaseEstimator],
    verbose: bool = False,
) -> Tuple[str, str, List[Tuple[BaseEstimator, float]]]:
    """
    Ray task which contains all logic necessary to load a data batch, transform it, 
    split it into train and test, and fit and evaluate models on it. We make sure to 
    return the file and location id used so that we can map the fitted models back to them.

    Args:
        file_name: str path to the parquet file holding transformed data to be trained
        pickup_location_id: int location id for the pick point
        models: list of BaseEstimators to train and fit all the models
    Returns:
        A tuple of file path, location id, and results
    """
    start_time = time.time()

    # Get batch data for specific pickup_location_id
    data = read_data(file_name, pickup_location_id)
    data_loading_time = time.time() - start_time
    if verbose:
        print_time_info_stats(
            f"Data loading time for LocID: {pickup_location_id}: {data_loading_time:.3f}"
        )

    # Perform transformation
    start_time = time.time()

    # Transform the batch 
    data = transform_batch(data)
    transform_time = time.time() - start_time
    if verbose:
        print_time_info_stats(
            f"Data transform time for LocID: {pickup_location_id}: {transform_time:.3f}")

    # Perform training & evaluation for each model with this batch-id data set
    start_time = time.time()
    results = (train_and_evaluate_internal(data, models, pickup_location_id),)
    training_time = time.time() - start_time
    if verbose: 
        print_time_info_stats(
        f"Training time for LocID: {pickup_location_id}: {training_time:.3f}")

    return (
        file_name,
        pickup_location_id,
        results,
    )

def run_batch_training(files: List[str], models: List[BaseEstimator], verbose: bool=False)  -> \
            Tuple[Tuple[str, str, List[Tuple[BaseEstimator, float]]], Dict[Any, Any]]:
    """
    This function is the main driver. It does the following:
     1. From a list of parquet files, read each parquet file and select a pickup location id column
     2. For each pickup location, train and evaluate all the models 
     3. Fetch all the results by blocking ray.get

    Args:
        files: list of all parquet files holding NYC data
        models: list of sklearn BaseEstimators 
        verbose: bool for verbose output of times
    Returns:
        returns a tuple of file_name, location_id, list of models and its corrosponding MAE
    """
    print("Starting unoptimized run: each task reading each file into memory ...")

    start = time.time()

    # Store task references
    task_refs = []
    
    # For each file only fetch the pickup_location_id since we want
    # to train each model on this attribute's associated batch of data
    for file in files:
        try:
            locdf = pq.read_table(file, columns=["pickup_location_id"])
        except Exception:
            continue

        # Only process unique ids
        pickup_location_ids = locdf["pickup_location_id"].unique()

        # For each unique pickup location, train and fit each model
        for pickup_location_id in pickup_location_ids:
            # Cast PyArrow scalar to Python if needed.
            try:
                pickup_location_id = pickup_location_id.as_py()
            except Exception:
                pass
            task_refs.append(
                train_and_evaluate.remote(file, pickup_location_id, models, verbose=verbose)
            )

    # Block to obtain results from each task
    results = ray.get(task_refs)

    taken = time.time() - start
    count = len(results)
    # If result is None, then it means there weren't enough records to train
    results_not_none = [x for x in results if x is not None]
    count_not_none = len(results_not_none)

    times_stats = {}
    times_stats["total_pickup_locations"] = count
    times_stats["total_pickup_locations_trained"] =  count_not_none
    times_stats["total_models_trained"] =  count_not_none * len(models)
    times_stats["total_training_time"] =  round(taken, 3)

    return results, times_stats
