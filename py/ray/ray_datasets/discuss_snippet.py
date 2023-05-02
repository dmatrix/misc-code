import ray
import pandas as pd

DATA_FOLDER = "fake_data"
OUTFILE = f"{DATA_FOLDER} / 'test.parquet'"

def func(batch):
    df = pd.DataFrame([{'a': d*2, 'b': d**4} for d in batch])
    return df

ds = ray.data.range(1000)
ds = ds.map_batches(func, zero_copy_batch=True)
print(ds.take(2))
print(ds.schema)

# write to disk 
ds.write_parquet(OUTFILE)
dataset = ray.data.read_parquet(OUTFILE)
result = dataset.take(2)
print(result)
print(dataset.schema)
