import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_model_info(m):
        print("--")
        print("name: {}".format(m.name))
        print("tags: {}".format(m.tags))
        print("description: {}".format(m.description))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()

    # Register a couple of models with respective names, tags, and descriptions
    for name, tags, desc in [("name1", {"t1": "t1"}, 'description1'),
                    ("name2", {"t2": "t2"}, 'description2')]:
        client.create_registered_model(name, tags, desc)

    # Fetch all registered models
    models = client.list_registered_models()
    for m in models:
        print_model_info(m)
