import numpy as np
import mlflow

QADict = {'What is your full name?': 'My name is King George.',
          'Have you taken your medication?': "I don't think so."}


class convEngine(mlflow.pyfunc.PythonModel):

    def __init__(self, QADict, model):
        self.model = model
        self.Qlist = list(QADict.keys())
        self.Qanswers = self.embed(self.Qlist)
        self.QADict = QADict

    def embed(self, input):
        return self.model(input)

    def predict(self, model_input_string):
        qasked = self.embed([model_input_string])
        corr = np.inner(qasked, self.Qanswers)
        index_max = np.argmax(corr)

        return self.QADict[self.Qlist[index_max]]


if __name__ == '__main__':

    import tensorflow_hub as hub
    import cloudpickle

    module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
    model = hub.load(module_url)
    model_path = "/tmp/tf_model"

    with open(model_path, "w+") as f:
        cloudpickle.dump(model, f)
    """
    convModel = convEngine(QADict, model)
    mlflow.pyfunc.save_model(path=model_path, python_model=convModel)
    """
