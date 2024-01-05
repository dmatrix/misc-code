from typing import List
import ray

# Define Ray remote functions.
@ray.remote
def read_data(num: int):
    # simulate reading data from a file or database.
    return [i+1 for i in range(num)]

@ray.remote
def preprocessing(data: List[float]) -> List[float]:
    # simulate preprocessing the data.
    return [(d**2) * d  for d in data]

@ray.remote
def aggregate(data: List[float]) -> float:
    # simulate aggregating the data.
    return sum(data)

if __name__ == "__main__":
    if not ray.is_initialized():
        ray.init()
    # Build the DAG:
    # data -> preprocessed_data -> aggregate
    data = read_data.bind(10)
    preprocessed_data = preprocessing.bind(data)
    output = aggregate.bind(preprocessed_data)

    # Execute the DAG and print the result.
    print(ray.get(output.execute()))