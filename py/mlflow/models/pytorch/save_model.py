import warnings
import os

import numpy as np
import torch
import mlflow.pytorch


class LinearNNModel(torch.nn.Module):

    def __init__(self):
       super(LinearNNModel, self).__init__()
       self.linear = torch.nn.Linear(1, 1)  # One in and one out

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred


if __name__ == '__main__':

    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    def gen_data():

        # Example linear model modified to use y = 2x
        # from https://github.com/hunkim/PyTorchZeroToAll/blob/master/05_linear_regression.py
        # X training data, y labels
        X = torch.arange(1.0, 25.0).view(-1, 1)
        y = torch.from_numpy(np.array([x * 2 for x in X])).view(-1, 1)
        return X, y

    # our model
    model = LinearNNModel()
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    # Training loop
    epochs = 250
    X, y = gen_data()
    for epoch in range(epochs):

        # Forward pass: Compute predicted y by passing X to the model
        y_pred = model(X)

        # Compute the loss
        loss = criterion(y_pred, y)

        # Zero gradients, perform a backward pass, and update the weights.
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 50 == 0:
            print('Epoch: {}/{}, loss: {:.4f}'.format(epoch + 1., epochs, loss.data.item()))

    # Save PyTorch models to current working directory
    with mlflow.start_run() as run:
        mlflow.pytorch.save_model(model, "models_pth")

        # Convert to a scripted model and save it
        scripted_pytorch_model = torch.jit.script(model)
        mlflow.pytorch.save_model(scripted_pytorch_model, "scripted_models_pth")

    # Load each saved model and inference
    print("--")
    for model_path in ["models_pth", "scripted_models_pth"]:
        model_uri = "{}/{}".format(os.getcwd(), model_path)
        loaded_model = mlflow.pytorch.load_model(model_uri)
        print("model: {}".format(model_path))
        for hv in [6.0, 8.0, 12.0, 30.0]:
            hour_var = torch.Tensor([[hv]])
            y_pred = loaded_model(hour_var)
            print("predict X:{}, y_pred: {:.2f}".format(hv, y_pred.data.item()))
        print("--")


