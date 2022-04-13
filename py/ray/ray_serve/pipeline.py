import os

from ray import serve
import mlflow


@serve.deployment
class Estimator:
    def __init__(self, model_uri):
        # Load an estimator model from the Model registry
        mlflow.set_tracking_uri(os.environ.get('MLFLOW_TRACKING_URI'))
        self.model = mlflow.sklearn.load_model(model_uri)

    def __call__(self, *args, **kwargs):
        return self.model.predict(args)


@serve.deployment
class PipelineSKLearn:
    def __init__(self, model_uri):
        # Load the sklearn pipeline model
        mlflow.set_tracking_uri(os.environ.get('MLFLOW_TRACKING_URI'))
        self.model = mlflow.sklearn.load_model(model_uri)

    def __call__(self, *args, **kwargs):
        return self.model.predict(args)


@serve.deployment
class Orchestrator:
    def __init__(self):
        self.estimator = Estimator.get_handle()
        self.pipeline = PipelineSKLearn.get_handle()

    async def __call__(self, *args, **kwargs):
        tranform_data = await self.estimator.remote(args)
        prediction = await self.pipeline.remote(tranform_data)
        return prediction


if __name__ == "__main__":
    serve.start()
    Estimator.deploy()
    PipelineSKLearn.deploy()
    Orchestrator.deploy

    serve.shutdown()


