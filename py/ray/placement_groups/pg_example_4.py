import ray
from ray.util.placement_group import (placement_group_table, placement_group)


@ray.remote
def child():
    return "C"


@ray.remote
def parent():
    # The child task is scheduled with the same placement group as its parent
    # although child.options(placement_group=pg).remote() wasn't called.
    ray.get(child.remote())


if __name__ == "__main__":
    ray.init()

    # Create a placement group with the STRICT_SPREAD strategy.
    pg = placement_group([{"CPU": 2}, {"CPU": 2}], strategy="STRICT_SPREAD")
    ready, unready = ray.wait([pg.ready()], timeout=5)
    print(f"placement group status:{ready}")
    print(placement_group_table(pg))

    # schedule parent and child
    print(ray.get(parent.options(placement_group=pg).remote()))
