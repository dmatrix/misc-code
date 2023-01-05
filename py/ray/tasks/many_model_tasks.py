from tqdm import tqdm
from time import time
from ray.util.multiprocessing import Pool
import ray

MAX_FILES_TO_READ=100               # Increase to 1M

@ray.remote
def train_model(file_path: str, verbose: bool=False) -> None:
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
    return lr

if __name__ == "__main__":

    if ray.is_initialized():
        ray.shutdown()
    ray.init()

    start = time()
    models_to_train = [
	    f"s3://anonymous@air-example-data/h2oai_1m_files/file_{i:07}.csv"
	    for i in range(MAX_FILES_TO_READ) ]

    # # Create a pool, where each worker is assigned 1 CPU by Ray.
    # pool = Pool(ray_remote_args={"num_cpus": 1})

    # # Use the pool to run `train_model` on the data, in batches of 10.
    # iterator = pool.imap_unordered(train_model, models_to_train, chunksize=10)
    
    # # Track the progress using tqdm and retrieve the results into a list.
    # list(tqdm(iterator, total=MAX_FILES_TO_READ))
    models_refs = [train_model.remote(f) for f in models_to_train]
    elapsed = time() - start
    done_models = []
    while len(models_refs) > 0:
        ready_models, models_refs = ray.wait(models_refs, num_returns=10)
        done_models.extend(ray.get(ready_models))

    results = ray.get(models_refs)
    print(f"Trained {len(done_models)} models in {elapsed:.2f} seconds")


