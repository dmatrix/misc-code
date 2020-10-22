import mlflow
from mlflow.tracking import MlflowClient

if __name__ == "__main__":

    def print_registered_model_info(rm):
        print("name: {}".format(rm.name))
        print("tags: {}".format(rm.tags))
        print("description: {}".format(rm.description))

    name = "SocialMediaTextAnalyzer"
    tags = {"nlp.framework": "Spark NLP"}
    desc = "This sentiment analysis model classifies the tone-happy, sad, angry."

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    client = MlflowClient()
    client.create_registered_model(name, tags, desc)
    print_registered_model_info(client.get_registered_model(name))
    print("--")

    # Update the model's description
    desc = "This sentiment analysis model classifies tweets' tone: happy, sad, angry."
    client.update_registered_model(name, desc)
    print_registered_model_info(client.get_registered_model(name))
