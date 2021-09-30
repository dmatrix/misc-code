import requests

from ray import serve


@serve.deployment
def hello(request):
    name  = request.query_params["name"]
    return f"Hello {name}!"


if __name__ == '__main__':

    # Start Ray serve within Ray on the local host
    serve.start()
    hello.deploy()

    # Query our endpoint over HTTP.
    for n in ["Jules", "Secunder", "Damji"]:
        response = requests.get(f"http://127.0.0.1:8000/hello?name={n}").text
        print(response)


