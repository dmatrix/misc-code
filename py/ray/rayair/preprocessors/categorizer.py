import ray
from pandas.api.types import CategoricalDtype
from ray.data.preprocessors import Categorizer
from data_utils import gen_pandas_data

if __name__ == "__main__":

    ds = ray.data.from_pandas(gen_pandas_data())

    print("----" * 5)
    print("dataset before first fit & transform categorical....")
    print(ds.show(5))

    # let's transform some dataset columns to categorical data type.
    categorical_columns = ["marital_status", "property", "gender", "state"]

    c1 = CategoricalDtype(categories=["married", "single", "domestic", "divorced", "undeclared"], ordered=False)
    c2 = CategoricalDtype(categories=["condo", "house", "rental", "cottage"], ordered=False)
    c3 = CategoricalDtype(categories=["F", "M", "U"], ordered=False)
    c4 = CategoricalDtype(categories=["CA", "AZ", "OR", "WA", "TX", "UT", "NV", "NM", ""], ordered=False)

    cat_dtypes =  {"marital_status": c1,
                    "property": c2,
                    "gender": c3,
                    "state": c4
                    }
                          

    preproc = Categorizer(columns=categorical_columns, dtypes=cat_dtypes)
    ds_transform = preproc.fit_transform(ds)

    print("----" * 5)
    print("dataset after first fit & transform categorical....")
    print(ds_transform.show(5))
    print(preproc.stats_)