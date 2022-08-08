import ray
from ray import serve
import requests

@serve.deployment
def hello(request):
    name = request.query_params["name"]
    return f"Hello {name}"


if __name__ == "__main__":

    handle = hello.bind()
    serve.run(handle)

    for i in range(10):
        response = requests.get(f"http://127.0.0.1:8000/hello?name=request_{i}").text
        print(f'{i:2d}: {response}')