import time
import numpy as np
import ray
from ray.util.placement_group import (placement_group_table, placement_group)


@ray.remote(num_cpus=1)
class CPUActor:
    def __init__(self):
        pass

    def actor_method(self, n):
        return np.random.rand(n, n)


@ray.remote(num_cpus=1)
# @ray.remote(resources={"extra_resource": 1})
def extra_resource_task(n):

    # Simulate long-running task.
    time.sleep(0.5)
    return np.random.rand(2*n, 2*n)


if __name__ == "__main__":
    bundle_1 = {"CPU": 2}
    bundle_2 = {"extra_resource": 2}

    ray.init(num_cpus=4, resources={"extra_resource": 2})

    # create a placement group and reserve 2 CPUs
    # Reserve bundles with strict pack strategy.
    # It means Ray will reserve 2 "GPU" and 2 "extra_resource" on the same
    # node (strict pack) within a Ray cluster. Using this placement group for scheduling actors
    # or tasks will guarantee that they will be colocated on the same node.
    pg = placement_group([bundle_1, bundle_2], strategy="SPREAD")

    # You can also use ray.wait.
    ready, unready = ray.wait([pg.ready()], timeout=5)
    print(f"placement group status:{ready}")
    print(placement_group_table(pg))

    # Create CPU actors on a cpu bundle.
    cpu_actors = [CPUActor.options(
        placement_group=pg,
        # This is the index from the original list.
        # This index is set to -1 by default, which means any available bundle.
        placement_group_bundle_index=0)  # Index of cpu_bundle is 0.
                      .remote() for _ in range(2)]
    actor_results = [a.actor_method.remote(2) for a in cpu_actors]
    print(f"Actor results: {ray.get(actor_results)}")

    # Create Tasks for the extra_resources
    cpu_tasks = [extra_resource_task.options(placement_group=pg, placement_group_bundle_index=1).remote(2) for _ in range(2)]

    print(f"Task results: {ray.get(cpu_tasks)}")





