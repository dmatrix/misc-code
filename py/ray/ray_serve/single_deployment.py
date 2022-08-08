from turtle import clear
import ray
from ray import serve
import requests
from random import random
import os
import starlette
from starlette.requests import Request

class Model:
    def __init__(self, path):
        self.path = path

    def predict(self, data: float) -> float:
        return random() + data if data > 0.5 else data


@serve.deployment
class Predictor:
    # Take in a path to load your desired model
    def __init__(self, path: str) -> None:
        self.path = path
        self.model = Model(path)
        # Get the pid on which this deployment is running on
        self.pid = os.getpid()

    # Deployments are callable. Here we simply return a prediction from our request.
    async def predict(self, data: float) -> str:
        pred = self.model.predict(data)
        return (f"(pid: {self.pid}); path: {self.path}; "
                f"data: {float(data):.3f}; prediction: {pred:.3f}")

    async def __call__(self, http_request: starlette.requests.Request) -> str:
        data = float(http_request.query_params['data'])
        return await self.predict(data)

if __name__ == "__main__":

    # predictor_1 = Predictor.options(name="rep-1", num_replicas=2).bind("/model/model-1.pkl")
    predictor_1 = Predictor.options(num_replicas=2).bind("/model/model-1.pkl")
    serve.run(predictor_1)

    print(serve.list_deployments())
    url = "http://127.0.0.1:8000/Predictor"    
    for _ in range(4):
        url = "http://127.0.0.1:8000/Predictor"    
        response =  requests.get(url, params={"data": random()})
        prediction = response.text
        print(f"prediction(via HTTP) : {prediction}")

    print("-----" * 5)

    svr_handle = Predictor.get_handle()
    # svr_handle = Predictor.get_handle("rep-1")
    print(svr_handle)

    for _ in range(4):
        print(f"prediction (via ServeHandle) : {ray.get(svr_handle.predict.remote(random()))}")