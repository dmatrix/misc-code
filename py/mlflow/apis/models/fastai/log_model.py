import os
import warnings
from fastai.vision import URLs, untar_data, ImageDataBunch, imagenet_stats, models, accuracy, rand_pad, cnn_learner
import mlflow.fastai
from mlflow.tracking import MlflowClient


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

   # Train and fit the Learner model
   learn = cnn_learner(data, models.resnet18, metrics=accuracy)

   # Start MLflow session
   with mlflow.start_run() as run:
       learn.fit(epochs, learning_rate)
       mlflow.fastai.log_model(learn, 'model')

   # fetch the logged model artifacts
   artifacts = [f.path for f in MlflowClient().list_artifacts(run.info.run_id, 'model')]
   print("artifacts: {}".format(artifacts))


if __name__ == '__main__':
   main(epochs=5, learning_rate=0.01)
