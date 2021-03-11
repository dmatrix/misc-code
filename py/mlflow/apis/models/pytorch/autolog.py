import os

import pytorch_lightning as pl
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import FashionMNIST
from pytorch_lightning.metrics.functional import accuracy

import mlflow.pytorch
from mlflow.tracking import MlflowClient

# Here's the simplest most minimal example with just a training loop
# (no validation, no testing). It illustrates how you can use MLflow
# to auto log parameters, metrics, and models.
# Explore the PyTorch FashionMNIST example for an expansive example with all the
# lightening hooks as the next step.


class MNISTModel(pl.LightningModule):

    def __init__(self):
        super(MNISTModel, self).__init__()
        self.l1 = torch.nn.Linear(28 * 28, 10)

    def forward(self, x):
        return torch.relu(self.l1(x.view(x.size(0), -1)))

    def training_step(self, batch, batch_nb):
        x, y = batch
        loss = F.cross_entropy(self(x), y)
        acc = accuracy(loss, y)
        self.log("train_loss", loss, on_epoch=True)
        self.log("acc", acc, on_epoch=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=0.02)


if __name__ == '__main__':

    def print_auto_logged_info(r):

        tags = {k: v for k, v in r.data.tags.items() if not k.startswith("mlflow.")}
        artifacts = [f.path for f in MlflowClient().list_artifacts(r.info.run_id, "model")]
        print("run_id: {}".format(r.info.run_id))
        print("artifacts: {}".format(artifacts))
        print("params: {}".format(r.data.params))
        print("metrics: {}".format(r.data.metrics))
        print("tags: {}".format(tags))

    # Avoid OMP error and allow multiple OpenMP runtime
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    # Init our model
    mnist_model = MNISTModel()

    # Init DataLoader from MNIST Dataset
    train_ds = FashionMNIST(os.getcwd(), train=True, download=True, transform=transforms.ToTensor())
    train_loader = DataLoader(train_ds, batch_size=32)

    # Initialize a trainer
    trainer = pl.Trainer(max_epochs=20, progress_bar_refresh_rate=20)

    # Auto log all MLflow entities
    mlflow.pytorch.autolog()

    # Train the model
    with mlflow.start_run() as run:
        trainer.fit(mnist_model, train_loader)

    # fetch the auto logged parameters and metrics
    print_auto_logged_info(mlflow.get_run(run_id=run.info.run_id))
