import ray
from ray.data.preprocessors import LabelEncoder
from data_utils import gen_pandas_data

if __name__ == "__main__":

    ds = ray.data.from_pandas(gen_pandas_data())

    print("----" * 5)
    print("dataset before first fit & transform label encoding....")
    print(ds.show(5))

    # Label encode two columns
    for label in ["marital_status", "property", "gender"]:
        print(f"Label encoding column:{label} ... ")
        preproc = LabelEncoder(label_column=label)
        ds = preproc.fit_transform(ds)

    print("----" * 5)
    print("dataset after first fit & transform label encoding....")
    print(ds.show(5))