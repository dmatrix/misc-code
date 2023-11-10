import ray

ds = ray.data.read_parquet("s3://anonymous@ray-example-data/iris.parquet")