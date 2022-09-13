import os
import ray
import random
from models import ModelWrapper, load_pickled_model

ENV_VARIABLES = {"S3_BUCKET": "/bucket/models",                     # public location in the cloud 
                 "LR_MODEL": "lr_model.pkl",                        # name of the model in the bucket
                  }
                
my_runtime_env = {"pip": ["scipy", "requests", "statsmodels"],      # Python packages dependencies
                  "env_vars": ENV_VARIABLES,                        # environment variables accessible to Ray tasks
                  "working_dir": "feature_files"                    # local directory uploaded and accessble to Ray tasks
}

@ray.remote
def model_predictions(bucket_name, name, use_files=False):
    # Access the enviroment variables
    model_name = os.environ.get(name)
    bucket_location = os.environ.get(bucket_name)
    if model_name and bucket_location:
        model_path = os.path.join(bucket_location, model_name)
        print(f"processing model: {model_name}")
        if use_files:
            m_name, _ = os.path.splitext(model_name)
            # The function will have its working directory changed to its node's
            # local copy of "feature_files", so the path are relative
            path = f"{m_name}.csv"
            print(f"processing files: {path}")
            model_path = f"{m_name}.pkl"
            # unpickle the model and invoke its predict function
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

    ray.init(runtime_env=my_runtime_env)
    PAIRS = (("S3_BUCKET","LR_MODEL"), ("NO_BUCKET","NO_MODEL"))
    restuls = [model_predictions.remote(b, n, True) for b, n in (PAIRS)]
    [print(f"predicted added value: {result:.2f}") for result in ray.get(restuls)]