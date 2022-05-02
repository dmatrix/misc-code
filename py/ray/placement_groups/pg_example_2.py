import time
import ray
from ray.util.placement_group import (placement_group_table, placement_group)


# Use or allocate two cpus for ths task
@ray.remote(num_cpus=2)
def func():
    return True


# Use or allocate two cpus for ths task
@ray.remote(num_cpus=2)
def func2():
    return True


if __name__ == "__main__":
    ray.init(num_cpus=2, resources={"extra_resources": 2})
    bundle_1 = {"CPU": 2}
    bundle_2 = {"extra_resources": 2}

    # create a placement group and reserve 2 CPUs
    # Reserve bundles with strict pack strategy.
    # It means Ray will reserve 2 "GPU" and 2 "extra_resource" on the same node (strict pack)
    # within a Ray cluster. Using this placement group for scheduling actors or tasks will
    # guarantee that they will be colocated on the same node.
    pg = placement_group([bundle_1, bundle_2], strategy="STRICT_PACK")

    # You can also use ray.wait.
    ready, unready = ray.wait([pg.ready()], timeout=5)
    print(f"placement group status:{ready}")
    print(placement_group_table(pg))

    # Now schedule remote task func() with its own request of two cups
    # which is not part of placement group. this won't work. You'll
    # get warning not being able to schedule this task
    try:
        print(ray.get(func.remote(), timeout=2))
    except ray.exceptions.GetTimeoutError:
        print("Timeout and could be scheduled")

    # Now let's make this task as part of the placement group
    print(ray.get(func2.options(placement_group=pg).remote()))
