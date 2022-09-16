import random
import pandas as pd
import time
import pickle
import os

import ray.data

def save_pickle_model(m, path):
    with open(path, 'wb') as f:
        pickle.dump(m, f)

def load_pickled_model(path):
    model = None
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model

class ModelWrapper:
    def __init__(self):
        
        self.features = None
        self.model = None

    def load_features(self, path):
        # self.features = ray.data.read_csv(path)
        self.features = pd.read_csv(path)

    def train(self, data):
        time.sleep(1.0)

    def predict(self):
        n_trips = self.features["num_trips"].item()
        miles = self.features["miles_covered"].item()
        value_added = (n_trips * miles) * random.random() / 100
        return value_added
    
    def save_model(self, path):
        # saving the model
        save_pickle_model(self, path)
    
    def load_model(self, path):
        # load the model
        self.model = load_pickled_model(path)

    
    
    
    
