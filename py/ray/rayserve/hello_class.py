import requests
from ray import serve
import starlette
from starlette.requests import Request


@serve.deployment
class HelloClass:
    def __init__(self):
        pass

    def echo(self, data):
        return f"Hello {data}!"

    def __call__(self, request):
        data = request.query_params['data']
        return self.echo(data)


if __name__ == '__main__':
    import ray
    
    hello_cls = HelloClass.options(name="hello").bind()
    serve.run(hello_cls)

    print(serve.list_deployments())

    # Query our endpoint over HTTP.
    for n in ["Jules", "Secunder", "Damji"]:
        response = requests.get(f"http://127.0.0.1:8000/HelloClass?data={n}").text
        print(response)


