import os
import warnings

from fastai.vision import URLs, untar_data, ImageDataBunch, imagenet_stats, models, accuracy, rand_pad, cnn_learner
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
   path = untar_data(URLs.MNIST_SAMPLE)

   # Prepare, transform, and normalize the data
   data = ImageDataBunch.from_folder(path, ds_tfms=(rand_pad(2, 28), []), bs=64)
   data.normalize(imagenet_stats)

   # Create CNN the Learner model
   learn = cnn_learner(data, models.resnet18, metrics=accuracy)

   # Start MLflow session
   with mlflow.start_run() as run:
       learn.fit(epochs, learning_rate)
       mlflow.fastai.log_model(learn, "model")

   # load the model for scoring
   model_uri = "runs:/{}/model".format(run.info.run_id)
   loaded_model = mlflow.fastai.load_model(model_uri)

   predict_data = ...
   loaded_model.predict(predict_data)


if __name__ == '__main__':
   main(epochs=1, learning_rate=.01)

