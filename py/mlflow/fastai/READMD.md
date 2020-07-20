## MLflow Project with Fastai 

This simple example illustrates how you can use `mlflow.fastai.autolog()` API
to train a simple MNIST model. Derived from fastai GitHub Repository of [vision examples](https://github.com/fastai/fastai/blob/master/examples/vision.ipynb),
we modified to run as an MLflow project, with either default or supplied arguments. The default arguments are
learning rate(`lr=0.01`) and number of epochs (`epochs=5`)

### How to run 

You can run this MLflow project fastai example in two  ways:

1. Run from the current git directory with default arguments.

 `mlflow run . -e main `
 `mlflow run . -e main -P lr=0.02 -P epochs=8`
 
2. Run from outside git repository

 `mlflow run https://github.com/mlflow/\#examples/fastai`
 `mlflow run https://github.com/mlflow/\#examples/fastai -P lr=0.02 -P epochs=8`
 
Both these runs will create an `mlruns` directory at the same level where you ran
these commands. To launch an MLflow UI to inspect the parameters, metrics, and artifacts automatically
logged by the `mflow.fastai.autolog()`, launch the MLflow UI: `mlflow ui`, and in your brower connect 
`localhost:5000 or 127.0.0.1:5000`
