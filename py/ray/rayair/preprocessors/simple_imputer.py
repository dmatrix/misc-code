import random
import ray
from ray.data.preprocessors import SimpleImputer
from data_utils import get_anonomized_name, get_anonomized_ssn, generate_data


if __name__ == "__main__":

        items = generate_data()

        # Before imputing 
        ds = ray.data.from_items(items)
        print("dataset before imputing....")
        print(ds.show(10))
        # after imputing
        preproc_1 = SimpleImputer(["dependents"], strategy="constant", fill_value=random.randint(1, 5))
        ds_trans = preproc_1.fit_transform(ds)
        print("----" * 5)
        print("dataset after first fit & transform imputing....")
        ds_trans.show(10)

        preproc_2 = SimpleImputer(["state"], strategy="most_frequent")
        ds_trans = preproc_2.fit_transform(ds_trans)

        print("dataset after second fit & transform imputing....")
        ds_trans.show(10)

        preproc_3 = SimpleImputer(["ssn"], strategy="constant", fill_value=get_anonomized_ssn())
        ds_trans = preproc_3.fit_transform(ds_trans)

        preproc_4 = SimpleImputer(["name"], strategy="constant", fill_value=get_anonomized_name())

        ds_trans = preproc_4.fit_transform(ds_trans)

        print("----" * 5)
        print("dataset after third fit & transform imputing....")
        ds_trans.show(10)