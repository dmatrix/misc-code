import argparse
import pandas as pd
import fastai.text as ftxt
import mlflow.fastai

def main():
    path = ftxt.untar_data(ftxt.URLs.IMDB_SAMPLE)
    df = pd.read_csv(path/'texts.csv')
    # Language model data
    data_lm = ftxt.TextLMDataBunch.from_csv(path, 'texts.csv')
    # Classifier model data
    data_clas = ftxt.TextClasDataBunch.from_csv(path, 'texts.csv', vocab=data_lm.train_ds.vocab, bs=32)

    learn = ftxt.language_model_learner(data_lm, ftxt.AWD_LSTM, drop_mult=0.5)
    # enable auto logging
    mlflow.fastai.autolog()

    # start MLflow session
    with mlflow.start_run():
        learn.fit_one_cycle(1, 1e-2)
    print(learn.predict("This is a review about", n_words=10))

if __name__ == '__main__':
   main()
