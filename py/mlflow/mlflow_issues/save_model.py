import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn import tree

if __name__ == '__main__':

    iris = load_iris()
    sk_model = tree.DecisionTreeClassifier()
    sk_model = sk_model.fit(iris.data, iris.target)

    sk_path = 'saved_models'
    mlflow.set_tracking_uri('sqlite:///mlruns.db')
    with mlflow.start_run() as run:
        mlflow.log_metric('m', 1.5)
        mlflow.sklearn.save_model(sk_model, sk_path)

    # Register model
    model_uri = "runs:/{}/saved_models".format(run.info.run_id)
    registered_model_name = "RegisterSavedModel"
    mv = mlflow.register_model(model_uri, registered_model_name)
    print("Name: {}".format(mv.name))
    print("Version: {}".format(mv.version))
