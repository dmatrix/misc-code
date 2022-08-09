import random

import requests
from ray import serve
from fastapi import FastAPI, Request

app = FastAPI()


@serve.deployment(route_prefix="/fapi")
@serve.ingress(app)
class FastAPIDeploymentExample:
    def __init__(self):
        self.prediction = random.random()

    @app.get("/predict")
    def get_prediction(self):
        return self.prediction

    @app.post("/update")
    def update(self, starlette_request:Request):
        data = float(starlette_request.query_params["data"])
        self.prediction += data


if __name__ == '__main__':
    serve.start()
    FastAPIDeploymentExample.deploy()
    resp = requests.get("http://127.0.0.1:8000/fapi/predict")
    print(resp.text)

    value = random.random() * 100
    print(f"Sending post request: {value}")
    resp = requests.post("http://127.0.0.1:8000/fapi/update", params={'data': value})

    resp = requests.get("http://127.0.0.1:8000/fapi/predict")
    print(resp.text)

