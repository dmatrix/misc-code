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
        preproc_2 = SimpleImputer(["state"], strategy="most_frequent")
        preproc_3 = SimpleImputer(["ssn"], strategy="constant", fill_value=get_anonomized_ssn())
        preproc_4 = SimpleImputer(["name"], strategy="constant", fill_value=get_anonomized_name())

        print("----" * 5)
        print("dataset before chained transforms ....")
        ds.show(10)

        # Now let's chain all of them together 
        chained_preproc = ray.data.preprocessors.Chain(preproc_1, preproc_2, preproc_3, preproc_4)
        ds_chained = chained_preproc.fit_transform(ds)

        print("----" * 5)
        print("dataset after chained transforms....")
        ds_chained.show(10)



