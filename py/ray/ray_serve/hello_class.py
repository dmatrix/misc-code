import requests
from ray import serve


@serve.deployment
class HelloClass:
    def __init__(self):
        pass

    def __call__(self, request):
        name = request.query_params["name"]
        return f"Hello {name}!"


if __name__ == '__main__':
    import ray
    # Start Ray serve within Ray on the local host
    ray.init(namespace="anonymous")
    serve.start(detached=True)
    HelloClass.deploy()

    # Query our endpoint over HTTP.
    for n in ["Jules", "Secunder", "Damji"]:
        response = requests.get(f"http://127.0.0.1:8000/HelloClass?name={n}").text
        print(response)


