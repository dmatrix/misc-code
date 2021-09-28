import numpy as np
from progressbar import progressbar
from sklearn import datasets
from sklearn.neural_network import MLPClassifier
import time
import ray


@ray.remote
def train_model(X, y, alpha):
    mlp = MLPClassifier(solver='sgd', alpha=alpha, max_iter=int(1e6), tol=1e-6,
                        hidden_layer_sizes=(5, 2), random_state=1)
    mlp.fit(X,y)
    return mlp.score(X, y)


if __name__ == '__main__':

    # Initialize Ray
    ray.init()          # default local mode

    # Create our dataset
    X, y = datasets.make_circles(n_samples=3 * 10**4, noise=0.5, factor=0.5, random_state=1)

    result_ids = [train_model.remote(X, y, alpha) for alpha in 10 ** np.linspace(-5, 5, 1000)]

    for result_id in progressbar(result_ids):
        ray.get(result_id)

    #time.sleep(1000)
