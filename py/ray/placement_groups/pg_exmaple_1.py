import time
import ray
from ray.util.placement_group import (placement_group, placement_group_table, remove_placement_group)

if __name__ == "__main__":
    ray.init(num_cpus=2, resources={"extra_resources": 2})
    bundle_1 = {"CPU": 2}
    bundle_2 = {"extra_resources": 2}

    pg = placement_group([bundle_1, bundle_2], strategy="STRICT_PACK")

    # You can also use ray.wait.
    ready, unready = ray.wait([pg.ready()], timeout=5)
    print(f"placement group status:{ready}")
    print(placement_group_table(pg))

    time.sleep(10)