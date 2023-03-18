
import numpy as np
from random import randint
import time
import ray

def load_model_A():
    def model(batch: dict) -> dict:
        
        model.payload = np.arange(100, 100_000_000, dtype=float)
        model.cls = "regression"
        model.bias = 4.5

        return  {"score": batch.get("passenger_count") + randint(1, 5) + model.bias}

    return model

def load_model_B():
    def model(batch: dict) -> dict:
        
        return  {"score": batch.get("passenger_count") + randint(1, 5) + model.bias}
    
    model.payload = np.arange(100, 100_000_000, dtype=float)
    model.cls = "regression"
    model.bias = 4.5

    return model

if __name__ == "__main__":

    d = {"passenger_count": randint(1, 5)}
    model_a = load_model_A()
    print(f"Model_A: Attribute cls: {getattr(model_a, 'cls', 'blah')}")
    print(f"Model_A: Attribute payload: {getattr(model_a, 'payload', 'blah')}")
    print(f"Model_A: pred payload: { model_a(d)}")
    
    print("--" * 5)

    model_b = load_model_B()
    print(f"Model_B: Attribute cls: {getattr(model_b, 'cls', 'blah')}")
    print(f"Model_B: Attribute payload: {getattr(model_b, 'payload', 'blah')}")
    print(f"Model_A: pred payload: { model_b(d)}")

