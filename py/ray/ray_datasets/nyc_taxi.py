import ray

if __name__ == "__main__":
    ray.init()

    ny_taxi_ds = ray.data.read_parquet("s3://ursa-labs-taxi-data/2009/01/data.parquet")
    print(ny_taxi_ds.count())