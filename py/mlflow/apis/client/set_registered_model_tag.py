import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_model_info(rm):
        print("--")
        print("name: {}".format(rm.name))
        print("tags: {}".format(rm.tags))

    name = "SocialMediaTextAnalyzer"
    tags = {"nlp.framework1": "Spark NLP"}
    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()

    # Create registered model, set an additional tag, and fetch
    # update model info
    client.create_registered_model(name, tags)
    model = client.get_registered_model(name)
    print_model_info(model)
    client.set_registered_model_tag(name, "nlp.framework2", "VADER")
    model = client.get_registered_model(name)
    print_model_info(model)
