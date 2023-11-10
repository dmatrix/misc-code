import ray
import time

if __name__ == "__main__":
    ray.init(num_cpus=5)

    ny_taxi_ds = ray.data.read_parquet("s3://ursa-labs-taxi-data/2009/01/data.parquet", parallelism=4).repartition(4)
    # print(ny_taxi_ds.take_batch(3))
    # shards = ny_taxi_ds.split(4)
    # print(shards)
    # print(ny_taxi_ds.count())
    # print(ray.put(shards))
    # # time.sleep(100)

    