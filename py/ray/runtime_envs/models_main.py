import os
from models import ModelWrapper, load_pickled_model, save_pickle_model

if __name__ == "__main__":
    m = ModelWrapper()
    m.load_features("feature_files/lr_model.csv")
    print(f"predicted added value: {m.predict():.2f}")
    save_pickle_model(m, os.path.abspath("feature_files/lr_model.pkl"))

    # load the model from pickle
    path = os.path.abspath("feature_files/lr_model.pkl")
    model = load_pickled_model(path)
    model.load_features(os.path.abspath("feature_files/lr_model_2.csv"))
    print(f"predicted added value: {model.predict():.2f}")
