import ray
from ray.util.scheduling_strategies import PlacementGroupSchedulingStrategy
from ray.util.placement_group import (placement_group_table, placement_group)


@ray.remote
def child():
    print(f"p_id:{ray.get_runtime_context().get_placement_group_id()}")
    print(f"task id: {ray.get_runtime_context().get_task_id()}")
    return "Child task is running with the parent's placement group."


@ray.remote
def parent():
    # The child task is scheduled with the same placement group as its parent
    # although child.options(...) was not called.
    return ray.get(child.remote())


if __name__ == "__main__":
    ray.init(num_cpus=5)

    # Create a placement group with the STRICT_SPREAD strategy.
    pg = placement_group([{"CPU": 2}, {"CPU": 2}], strategy="SPREAD")
    ready, unready = ray.wait([pg.ready()], timeout=5)
    print(f"placement group status:{ready}")
    print(placement_group_table(pg))
    print(f"Placement group id: {placement_group_table(pg)['placement_group_id']}")
    
    # schedule parent and child
    print(ray.get(parent.options(scheduling_strategy=PlacementGroupSchedulingStrategy(
        placement_group=pg,
        placement_group_bundle_index=0)).remote()))
