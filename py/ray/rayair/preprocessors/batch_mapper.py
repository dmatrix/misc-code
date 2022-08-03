import ray
import random
from ray.data.preprocessors import BatchMapper
from data_utils import gen_pandas_data

def increment_column(df, name):
    df[name] = df[name] * random.randint(100, 300)
    return df

if __name__ == "__main__":


    ds = ray.data.from_pandas(gen_pandas_data())
    print(ds.show(5))

    batch_preproc = BatchMapper(lambda df: increment_column(df, "amount"))
    df_trans = batch_preproc.fit_transform(ds)
    print(df_trans.show(5))
    
    