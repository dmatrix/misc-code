## MLflow Project: Fastai Example

This simple example illustrates how you can use `mlflow.fastai.autolog()` API
to track parameters, metrics, and artifacts while training a simple MNIST model. Derived from fastai GitHub Repository 
of [vision examples](https://github.com/fastai/fastai/blob/master/examples/train_mnist.py), the code is modified to run 
as an MLflow project, with either default or supplied arguments. The default arguments are learning rate(`lr=0.01`) 
and number of epochs (`epochs=5`).

You can use this example as a template and attempt advanced examples in
[Fastai tutorials](https://docs.fast.ai/vision.html), using `mlfow.fastai` model flavor and MLflow tracking API to
track your experiments.

### How to run 

You can run this MLflow project fastai example with default or supplied arguments in two  ways:

1. Run from the current git directory

 `mlflow run . -e main`
 `mlflow run . -e main -P lr=0.02 -P epochs=8`
 
2. Run from outside git repository

 `mlflow run https://github.com/mlflow/\#examples/fastai`
 `mlflow run https://github.com/mlflow/\#examples/fastai -P lr=0.02 -P epochs=8`
 
Both runs will create an `mlruns` directory at the same directory level where you ran
these commands. To launch an MLflow UI to inspect the parameters, metrics, and artifacts automatically
logged by the `mflow.fastai.autolog()`, launch the MLflow UI: `mlflow ui`, and in your brower, connect 
to `localhost:5000 or 127.0.0.1:5000`.
