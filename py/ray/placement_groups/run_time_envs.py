import os
import ray
import random
from models import ModelWrapper, load_pickled_model
from ray.runtime_env import RuntimeEnv

ENV__VARIABLES = {"S3_BUCKET": "/bucket/models",
                 "LR_MODEL": "lr_model.pkl",
                  }

my_runtime_env = RuntimeEnv(
    conda={
        "dependencies": 
        ["pip", {
            "pip": ["numpy"]
        }]
    },
    env_vars=ENV__VARIABLES
)

@ray.remote
def do_model_predictions(bucket_name, name, use_files=False):
    model_name = os.environ.get(name)
    bucket_location = os.environ.get(bucket_name)
    if model_name and bucket_location:
        model_path = os.path.join(bucket_location, model_name)
        print(f"processing model: {model_name}")
        if use_files:
            m_name, _ = os.path.splitext(model_name)
            path = f"{m_name}.csv"
            print(f"processing files: {path}")
            model_path = f"{m_name}.pkl"
            model_wrapper = load_pickled_model(model_path)
            model_wrapper.load_features(path)
            return model_wrapper.predict()
        else:
            # don't use the pickled models; just for testing env variables
            return random.random()
    else:
        # we could not fetch the environment variables
        return -1

if __name__ == "__main__":
    # run it first without the runtme_env key word argument to ray.init()
    # the Ray tasks will all return -1 since they can't env variables
    # are not accessible
    #ray.init()

    # Uncomment and run with runtime_env set
    # set the working_dir to "." to push the feature_files and other content
    # that you might want to access.
    ray.init(runtime_env=my_runtime_env)
    PAIRS = (("S3_BUCKET","LR_MODEL"), ("NO_BUCKET","NO_MODEL"))
    restuls = [do_model_predictions.remote(b, n, True) for b, n in (PAIRS)]
    [print(f"predicted added value: {result:.2f}") for result in ray.get(restuls)]