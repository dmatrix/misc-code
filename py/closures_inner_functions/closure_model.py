import pandas as pd
import numpy as np
from random import randint
import time
import ray

def load_model():
    # A dummy model
    def model(batch: dict) -> dict:
        # Dummy payload so copying the model will actually copy some data
        # across nodes.
        model.payload = np.arange(100, 100_000_000, dtype=float)
        model.cls = "regression"
        print(f"Model: Has attribute cls: {hasattr(model, 'cls')}")
        print(f"Model: Has attribute payload: {hasattr(model, 'payload')}")
        
        return  {"score": batch.get("passenger_count") + randint(1, 5)}

    return model

@ray.remote
def make_pred(m, d):
    pred = m(d)
    return pred

if __name__ == "__main__":

    if ray.is_initialized():
        ray.shutdown()
    ray.init()

    m = load_model()
    print(f"Attribute cls: {getattr(m, 'cls', 'blah')}")
    print(f"Attribute payload: {getattr(m, 'payload', 'blah')}")
    
    model_ref = ray.put(m)

    result_refs = [make_pred.remote(model_ref, {"passenger_count": i + randint(1, 5)}) for i in range(6)]
    results = ray.get(result_refs)

    # Let's check prediction output size.
    for r in results:
        print(f"Prediction: {r}")

    # time.sleep(1000)
    ray.shutdown()
    