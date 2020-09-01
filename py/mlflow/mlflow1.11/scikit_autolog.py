from pprint import pprint
import numpy as np
import sklearn.linear_model
import mlflow

# enable autologging
mlflow.set_tracking_uri("sqlite:///mlruns.db")

mlflow.sklearn.autolog()

# prepare training data
X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3


def fetch_logged_data(run_id):
    client = mlflow.tracking.MlflowClient()

    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    metrics = {k: v for k, v in data.metrics.items()}
    params = {k: v for k, v in data.params.items()}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]

    return (params, metrics, tags, artifacts)

if __name__ == '__main__':
    # train a model
    with mlflow.start_run() as run:
        reg = sklearn.linear_model.LinearRegression().fit(X, y)

        # fetch logged data
        params, metrics, tags, artifacts = fetch_logged_data(run._info.run_id)

        # {'copy_X': 'True',
        #  'fit_intercept': 'True',
        #  'n_jobs': 'None',
        #  'normalize': 'False'}
        pprint(params)

        # {'training_score': 1.0}
        pprint(metrics)

        # {'estimator_class': 'sklearn.linear_model._base.LinearRegression',
        #  'estimator_name': 'LinearRegression'}
        pprint(tags)

        # ['model/MLmodel', 'model/conda.yaml', 'model/model.pkl', 'model/input_example.json']
        pprint(artifacts)
