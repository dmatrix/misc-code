import ray
from smart_open import smart_open
import pandas as pd

df = pd.read_csv(smart_open("s3://air-example-data/h2oai_1m_files/file_0000001.csv", "r"))
print(df[:5])
# ds = ray.data.read_csv("s3://anonymous@air-example-data/h2oai_1m_files/file_0000001.csv")
# df = ds.to_pandas()
# print(df[:3])