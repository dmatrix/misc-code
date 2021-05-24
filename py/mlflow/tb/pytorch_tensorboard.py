from torch.utils.tensorboard import SummaryWriter
import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets, transforms
import mlflow

import numpy as np

if __name__ == '__main__':

    writer = SummaryWriter()

    for n_iter in range(100):
        writer.add_scalar('Loss/train', np.random.random(), n_iter)
        writer.add_scalar('Loss/test', np.random.random(), n_iter)
        writer.add_scalar('Accuracy/train', np.random.random(), n_iter)
        writer.add_scalar('Accuracy/test', np.random.random(), n_iter)

    # Writer will output to ./runs/ directory by default
    writer = SummaryWriter()

    # Transformation pipeline applied to the input data
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # Create a PyTorch FashionMNIST dataset
    trainset = datasets.FashionMNIST('mnist_train', train=True, download=True, transform=transform)
    # Use the dataset as in the Dataloader
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)
    model = torchvision.models.resnet50(False)

    # Have ResNet model take in grayscale rather than RGB
    model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    images, labels = next(iter(trainloader))

    grid = torchvision.utils.make_grid(images)
    writer.add_image('images', grid, 0)
    writer.add_graph(model, images)
    writer.close()
    mlflow.start_run()
    mlflow.pytorch.load_model(model)
    mlflow.log_artifact("./runs")
    mlflow.end_run()


