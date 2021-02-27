import os
from argparse import ArgumentParser

import torch
from torchvision import transforms
import pytorch_lightning as pl
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks import LearningRateMonitor

import mlflow.pytorch


class LightningMNISTClassifier(pl.LightningModule):
    def __init__(self, **kwargs):
        """
        Initializes the network
        """
        super(LightningMNISTClassifier, self).__init__()

        # mnist images are (1, 28, 28) (channels, width, height)
        self.layer_1 = torch.nn.Linear(28 * 28, 128)
        self.layer_2 = torch.nn.Linear(128, 256)
        self.layer_3 = torch.nn.Linear(256, 10)
        self.args = kwargs
        # transforms for images
        self.transform = transforms.Compose(
            [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
        )

    def forward(self, x):
        """
        Forward Function
        """
        batch_size, channels, width, height = x.size()

        # (b, 1, 28, 28) -> (b, 1*28*28)
        x = x.view(batch_size, -1)

        # layer 1 (b, 1*28*28) -> (b, 128)
        x = self.layer_1(x)
        x = torch.relu(x)

        # layer 2 (b, 128) -> (b, 256)
        x = self.layer_2(x)
        x = torch.relu(x)

        # layer 3 (b, 256) -> (b, 10)
        x = self.layer_3(x)

        # probability distribution over labels
        x = torch.log_softmax(x, dim=1)

        return x

    @staticmethod
    def add_model_specific_args(parent_parser):

        parser = ArgumentParser(parents=[parent_parser], add_help=False)

        # Add trainer specific arguments
        parser.add_argument(
            "--tracking_uri", type=str, default="http://localhost:5000/", help="mlflow tracking uri"
        )
        parser.add_argument(
            "--max_epochs", type=int, default=20, help="number of epochs to run (default: 20)"
        )
        parser.add_argument(
            "--gpus", type=int, default=0, help="Number of gpus - by default runs on CPU"
        )
        parser.add_argument(
            "--accelerator",
            type=str,
            default=None,
            help="accelerator - (default: None)",
        )
        return parser


if __name__ == "__main__":
    parent_parser = ArgumentParser(description="PyTorch Autolog Mnist Example")

    parser = LightningMNISTClassifier.add_model_specific_args(parent_parser=parent_parser)

    mlflow.pytorch.autolog()  # just add this line and your Autologging should work!

    args = parser.parse_args()

    args = parser.parse_args()
    dict_args = vars(args)

    # mlflow.set_tracking_uri(dict_args['tracking_uri'])

    model = LightningMNISTClassifier(**dict_args)
    early_stopping = EarlyStopping(monitor="val_loss", mode="min", verbose=True)

    checkpoint_callback = ModelCheckpoint(
        filepath=os.getcwd(),
        save_top_k=1,
        verbose=True,
        monitor="val_loss",
        mode="min",
        prefix=""
    )
    lr_logger = LearningRateMonitor()

    trainer = pl.Trainer.from_argparse_args(
        args,
        callbacks=[lr_logger, early_stopping],
        checkpoint_callback=checkpoint_callback,
        # train_percent_check=0.1,
    )
    trainer.fit(model)
    trainer.test()



