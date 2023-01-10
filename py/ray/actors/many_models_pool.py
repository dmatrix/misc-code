from tqdm import tqdm
from time import time
from ray.util.multiprocessing import Pool
import ray

MAX_FILES_TO_READ = 10_000             # Increase to 1M

def train_model(file_path: str, verbose: bool=False) -> object:
    data_ds = ray.data.read_csv(file_path)
    data = data_ds.to_pandas()

    if verbose:
        print(f"Training model for file: {file_path}")
        print(data[:5])
        print(data.shape)

    # Train your model here
    from sklearn.linear_model import LinearRegression
    lr = LinearRegression()

    # Columns names are anonymized
    lr.fit(data[["id4", "id5"]], data["v3"])
    
    # Return a single dict of the model and stats, etc.
    return [{
        "coef": lr.coef_,
        "intercept": lr.intercept_,
        "customer_id": data["customer_id"][0],
    }]

if __name__ == "__main__":

    if ray.is_initialized():
        ray.shutdown()
    ray.init()
    fraction_of_cpus = 3
    num_cpus_available = ray.available_resources()["CPU"]
    num_pool_actors = int(num_cpus_available / fraction_of_cpus)

    start = time()
    models_to_train = [
	    f"s3://anonymous@air-example-data/h2oai_1m_files/file_{i:07}.csv"
	    for i in range(MAX_FILES_TO_READ) ]

    # Create a pool, where each worker is assigned 1 CPU by Ray.
    print(f"Using a pool of {num_pool_actors} of actors")
    pool = Pool(num_pool_actors, ray_remote_args={"num_cpus": 1})

    # Use the pool to run `train_model` on the data, in batches of 10.
    iterator = pool.imap_unordered(train_model, models_to_train, chunksize=5)
    
    # Track the progress using tqdm and retrieve the results into a list.
    results = list(tqdm(iterator, total=MAX_FILES_TO_READ))
    elapsed = time() - start
    print(f"Trained {MAX_FILES_TO_READ} models in {elapsed:.2f} seconds")
    print(f"Sample of lr models: {results[-2:]}")