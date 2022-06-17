import ray

if __name__ == "__main__":
    ray.init()

    ny_taxi_ds = ray.data.read_parquet(["s3://nyc-tlc/trip data/yellow_tripdata_2012-*.parquet"])
    print(ny_taxi_ds.count())