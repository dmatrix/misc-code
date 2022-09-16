import ray

runtime_env = {"conda": {"dependencies": ["pip", {"pip": ["scipy"]}]}}

ray.init(runtime_env=runtime_env)

@ray.remote
def f():
    import scipy
    return scipy.__version__

print(ray.get(f.remote()))