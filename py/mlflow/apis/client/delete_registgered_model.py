import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_registered_models_info(r_models):
        print("--")
        for rm in r_models:
            print("name: {}".format(rm.name))
            print("tags: {}".format(rm.tags))
            print("description: {}".format(rm.description))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()

    # Register a couple of models with respective names, tags, and descriptions
    for name, tags, desc in [("name1", {"t1": "t1"}, 'description1'),
                    ("name2", {"t2": "t2"}, 'description2')]:
        client.create_registered_model(name, tags, desc)

    # Fetch all registered models
    print_registered_models_info(client.list_registered_models())

    # Delete one registered model
    client.delete_registered_model("name1")
    print_registered_models_info(client.list_registered_models())
