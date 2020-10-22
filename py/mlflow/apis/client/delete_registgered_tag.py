import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_registered_models_info(r_models):
        print("--")
        for rm in r_models:
            print("name: {}".format(rm.name))
            print("tags: {}".format(rm.tags))

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()

    # Register a couple of models with respective names and tags
    for name, tags in [("name1", {"t1": "t1"}), ("name2", {"t2": "t2"})]:
        client.create_registered_model(name, tags)

    # Fetch all registered models
    print_registered_models_info(client.list_registered_models())

    # Delete a tag from model `name2`
    client.delete_registered_model_tag("name2", 't2')
    print_registered_models_info(client.list_registered_models())
