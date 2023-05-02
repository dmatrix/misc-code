import ray
import pandas as pd

DATA_FOLDER = "fake_data"
OUTFILE = f"{DATA_FOLDER} / 'test.parquet_2'"

def func(batch):
    df = pd.DataFrame([{'a': d*2, 'b': d**4} for d in range(batch)])
    return df

ds = ray.data.from_pandas(func(1000))
print(ds.take(2))
print(ds.schema)

# write to disk 
ds.write_parquet(OUTFILE)
dataset = ray.data.read_parquet(OUTFILE)
result = dataset.take(2)
print(result)
