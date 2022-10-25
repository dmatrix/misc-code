import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose(
    # this is the reason for normalizing (with mean, std) for each RGB channel
    # Normalization helps reduce or skewing and helps with faster CNN training
    # https://discuss.pytorch.org/t/understanding-transform-normalize/21730
    [transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))]
)


torchvision.datasets.CIFAR10(root="~/data", download=True, train=True, transform=transform)

torchvision.datasets.CIFAR10(root="~/data", download=True, train=False, transform=transform)