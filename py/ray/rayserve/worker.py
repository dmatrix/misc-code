import ray
from ray import serve
from random import randint
from math import pow
from starlette.requests import Request
import requests

import os

@serve.deployment
class Worker:

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, http_request):
        num = http_request.query_params["number"]
        return self.func(int(num))

if __name__ == __name__:

    # our function to pass to deployment
    func = lambda x: pow(x, 3)

    model_cls_node = Worker.bind("cubed", func)
    serve.run(model_cls_node)

    # send request 
    n = randint(1, 10)
    response = requests.get(f"http://127.0.0.1:8000/Worker?number={n}").text
    print(f"cubed of {n} is {response}")
