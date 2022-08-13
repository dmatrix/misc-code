import requests

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier

from ray import serve


@serve.deployment(route_prefix="/iris")
class BoostingModel:
    def __init__(self, model):
        self.model = model
        self.label_list = iris_dataset["target_names"].tolist()

    async def __call__(self, request):
        payload = await request.json()
        print(f"Received flask request with data {payload}")

        prediction = self.model.predict([payload["vector"]])[0]
        human_name = self.label_list[prediction]
        return {"result": human_name}

if __name__ == "__main__":

    # Train model.
    iris_dataset = load_iris()
    model = GradientBoostingClassifier()
    model.fit(iris_dataset["data"], iris_dataset["target"])

    # Deploy model
    srv_handle = BoostingModel.bind(model)
    serve.run(srv_handle)

    # Query model
    sample_request_input = {"vector": [1.2, 1.0, 1.1, 0.9]}
    response = requests.get("http://localhost:8000/iris", json=sample_request_input)
    print(response.text)
    
    # prints
    # Result:
    # {"result": "versicolor"}