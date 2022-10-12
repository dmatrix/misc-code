
from typing import Tuple
import pandas as pd
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms

from ray import train
from ray.data.extensions import TensorArray
from ray.air import session
from ray.train.torch import TorchCheckpoint
from ray.serve.http_adapters import NdArray
import matplotlib.pyplot as plt

CLASSES = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

transform = transforms.Compose(
    # this is the reason for normalizing (with mean, std) for each RGB channel
    # Normalization helps reduce or skewing and helps with faster CNN training
    # https://discuss.pytorch.org/t/understanding-transform-normalize/21730
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)

def train_dataset_factory():
    return torchvision.datasets.CIFAR10(root="./data", download=True, train=True, transform=transform)

def test_dataset_factory():
    return torchvision.datasets.CIFAR10(root="./data", download=True, train=False, transform=transform)

def convert_batch_to_pandas(batch: Tuple[torch.Tensor, int]) -> pd.DataFrame:
    images = [image.numpy() for image, _ in batch]
    labels = [label for _, label in batch]
    
    return pd.DataFrame({"image": images, "label": labels})

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # look for the meaning of the parameters on Conv()
        # https://stackoverflow.com/questions/56675943/meaning-of-parameters-in-torch-nn-conv2d
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Net2(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # output: 64 x 16 x 16

            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # output: 128 x 8 x 8

            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # output: 256 x 4 x 4

            nn.Flatten(), 
            nn.Linear(256*4*4, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 10))
        
    def forward(self, xb):
        return self.network(xb)

#
# Regular PyTorch training loop wrapped with some AIR code
# The training function will run on each worker
def train_loop_per_worker(config):
   
   # prepare the model for distributed training
    model = train.torch.prepare_model(Net())

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), config.get("lr", 0.001), momentum=0.9)

    # get the train dataset shard from the session implicity created for the
    # PyTorch Trainer
    train_dataset_shard = session.get_dataset_shard("train")
    
    # train over epoch
    print(f"configs to the trainer={config}")
    for epoch in range(config.get("epochs", 50)):
        running_loss = 0.0
        train_dataset_batches = train_dataset_shard.iter_torch_batches(
            batch_size=config.get("batch_size", 16)
        )
        # enumerate over each batch in the shard and train the model
        for i, batch in enumerate(train_dataset_batches):
            # get the inputs and labels
            inputs, labels = batch["image"], batch["label"]
            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            # compute the loss
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print some statistics along the way
            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print(f"[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}")
                running_loss = 0.0

        # Use the session to report loss and save the state dict
        run_loss_metrics = dict(train_loss=running_loss)
        torch_checkpoint = TorchCheckpoint.from_state_dict(model.module.state_dict())
        session.report(metrics=run_loss_metrics, checkpoint=torch_checkpoint)

def convert_logits_to_classes(df):
    best_class = df["predictions"].map(lambda x: x.argmax())
    df["prediction"] = best_class
    return df
    
def calculate_prediction_scores(df):
    df["correct"] = df["prediction"] == df["label"]
    return df[["prediction", "label", "correct"]]

def json_to_numpy(payload: NdArray) -> pd.DataFrame:
      """Accepts an NdArray JSON from an HTTP body and converts it to a Numpy Array."""
      # Have to explicitly convert to float since np.array reads as a double.
      arr = np.array(payload.array, dtype=np.float32)
      return arr

def to_prediction_cls(lst):
    max_value = max(lst)
    idx = lst.index(max_value)
    cls = CLASSES[idx] 
    return idx,cls

def img_show(img):
    img = img / 2 + 0.5     # unnormalize
    # npimg = img.numpy()
    plt.imshow(np.transpose(img, (1, 2, 0)))
    plt.show()