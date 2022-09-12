import os
import random

import ray
from ray.runtime_env import RuntimeEnv


ENV__VARIABLES = {"S3_BUCKET": "/bucket/models",
                 "LR_MODEL": "lr_model.pkl",
                  }

my_runtime_env = RuntimeEnv(
    conda={
        "dependencies": 
        ["pip", {
            "pip": ["scipy"]
        }]
    },
    env_vars=ENV__VARIABLES
)

@ray.remote
def func(m_name, bucket_name):
    import scipy

    model_name = os.environ.get(m_name)
    bucket_location = os.environ.get(bucket_name)
    if model_name and bucket_location:
        model_path = os.path.join(bucket_location, model_name)
        print(f"processing model: {model_name} at  {model_path}")
        return scipy.__version__
    else:
        return -1

if __name__ == "__main__":
    
    ray.init(runtime_env=my_runtime_env)
    PAIRS = (("S3_BUCKET","LR_MODEL"), ("NO_BUCKET","NO_MODEL"))
    restuls = [func.remote(b, n) for b, n in (PAIRS)]
    [print(f"predicted added value: {result}") for result in ray.get(restuls)]