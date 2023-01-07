import ray
from smart_open import smart_open
import pandas as pd

# df = pd.read_csv(smart_open("s3://air-example-data/h2oai_1m_files/file_0000001.csv", "r"))
# print(df[:5])
# ds = ray.data.read_csv("s3://anonymous@air-example-data/h2oai_1m_files/file_0000001.csv")
# df = ds.to_pandas()
# print(df[:3])

ds = ray.data.read_csv("s3://air-example-data/h2oai_benchmark", parallelism=8, ray_remote_args={"num_cpus": 8})
df = ds.to_pandas()
print(df[:3])
print(df.shape)

ds = ds.repartition(500)

# Compute our (dummy) `customer_id` key as the concatenation of the
# `id3` and `v1` columns and then group the dataset by it.
ds = ds.add_column("customer_id", lambda r: r["id3"] + r["v1"].astype(str))
ds = ds.groupby("customer_id")