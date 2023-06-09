import os
import subprocess

import ray
import ray.util.scheduling_strategies

@ray.remote
def fn_remote(dataset_name, base_model_name=None):
    pid = os.getpid()
    base_model_name = (
        base_model_name or "RWKV-4-Pile-1B5"
    )
    base_model_url = f"https://huggingface.co/BlinkDL/{base_model_name.lower()}"
    subprocess.run(
        f"mkdir -p /tmp/models-{pid}; cd /tmp/models-{pid}; git clone {base_model_url}; ls '{base_model_name.lower()}'",
        shell=True,
        check=True,
    )
    subprocess.run(
        f'echo "pid {pid}: starting dataset download {dataset_name}"',
        shell=True,
        check=True,
    )

def force_on_node(node_id: str, remote_func_or_actor_class):
    scheduling_strategy = ray.util.scheduling_strategies.NodeAffinitySchedulingStrategy(
        node_id=node_id, soft=False
    )
    options = {"scheduling_strategy": scheduling_strategy,
               "num_cpus": 1}
    return remote_func_or_actor_class.options(**options)

def run_on_every_node(remote_func_or_actor_class, *remote_args, **remote_kwargs):
    refs = []
    for node in ray.nodes():
            if node["Alive"] and node["Resources"].get("CPU", None):
                refs.append(
                    force_on_node(node["NodeID"], remote_func_or_actor_class).remote("mongoDB",
                        *remote_args, **remote_kwargs
                    )
                )
    return ray.get(refs)

if __name__ == "__main__":
    ray.init()
    run_on_every_node(fn_remote)


