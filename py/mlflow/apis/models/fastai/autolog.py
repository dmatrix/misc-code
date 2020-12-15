import os
import warnings
import fastai.vision as vis
import mlflow.fastai
from mlflow.tracking import MlflowClient


def print_auto_logged_info(r):
   tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
   artifacts = [f.path for f in MlflowClient().list_artifacts(r.info.run_id, "model")]
   print("run_id: {}".format(r.info.run_id))
   print("artifacts: {}".format(artifacts))
   print("params: {}".format(r.data.params))
   print("metrics: {}".format(r.data.metrics))
   print("tags: {}".format(tags))


def main(epochs=5, learning_rate=0.01):
   # Avoid OMP error and allow multiple OpenMP runtime
   os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
   warnings.filterwarnings("ignore")
   print(mlflow.__version__)

   # Download and untar the MNIST data set
   path = vis.untar_data(vis.URLs.MNIST_SAMPLE)

   # Prepare, transform, and normalize the data
   data = vis.ImageDataBunch.from_folder(path, ds_tfms=(vis.rand_pad(2, 28), []), bs=64)
   data.normalize(vis.imagenet_stats)

   # Train and fit the Learner model
   learn = vis.cnn_learner(data, vis.models.resnet18, metrics=vis.accuracy)

   # Enable auto logging
   mlflow.fastai.autolog()

   # Start MLflow session
   with mlflow.start_run() as run:
      learn.fit(epochs, learning_rate)

   # fetch the auto logged parameters, metrics, and artifacts
   print_auto_logged_info(mlflow.get_run(run_id=run.info.run_id))


if __name__ == '__main__':
   main(epochs=1, learning_rate=0.01)
