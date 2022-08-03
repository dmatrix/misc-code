import ray
import random
from ray.data.preprocessors import Normalizer
from sklearn import preprocessing

if __name__ == "__main__":
    items = [{"col-1": i + random.randint(25, 1500), 
              "col-2": i + random.randint(50, 2500) * 2,
              "col-3": i + random.randint(75, 3500) * 3 } for i in range(100, 300)]
    ds = ray.data.from_items(items)
    print(ds.take(5))
    
    preproc = Normalizer(["col-1", "col-2", "col-3"], norm="max")
    ds_trans = preproc.fit_transform(ds)
    print(ds_trans.take(5))

