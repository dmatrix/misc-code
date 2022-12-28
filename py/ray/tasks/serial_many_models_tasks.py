import time
import sys
import random
import argparse
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pprint import pprint
from tqdm.auto import tqdm
from typing import List, Tuple
import ray

MAX_TASKS = 10000
BATCH_SIZE = 1000
NUM_BATCHES = int(MAX_TASKS / BATCH_SIZE)
MODEL_TYPE = 0              # 0 for LinearRegression (default) ; 1 for RandomForestRegressor
RUN_TYPE = "all"            # "serial", "dist", or "all", default=all

def process_distributed_tasks(obj_refs: List[object]) -> float:
    processed_refs = []
    waiting_refs = obj_refs
    while(len(waiting_refs) > 0):
        # update result_refs to only
        # track the remaining tasks.
        ready_refs, remaining_refs = ray.wait(waiting_refs, num_returns=BATCH_SIZE)
        new_refs = ready_refs
        processed_refs.extend(new_refs)
        waiting_refs = remaining_refs

    return ray.get(processed_refs[0])


def prepare_data() -> Tuple[float, float, float, float]:
    X, y = fetch_california_housing(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


def train_model(model, x_train, x_test, y_train, y_test) -> float:
    
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    score = mean_squared_error(y_test, y_pred)
    return score


@ray.remote
def train_model_distributed(model, x_train, x_test, y_train, y_test):
    return train_model(model, x_train, x_test, y_train, y_test)

def run_serially(m, x_tr:float, x_t: float, y_tr:float, y_t:float, num_tasks: int) -> List[float]:
    for _ in tqdm(range(num_tasks)):
        score = train_model(m, x_tr, x_t, y_tr, y_t)

    # they all will have the same MSE, just return the last one
    return score

def run_distributed(m, x_tr:float, x_t: float, y_tr:float, y_t:float, num_tasks: int) -> List[float]:
    results = [train_model_distributed.remote(m, x_tr, x_t, y_tr, y_t) for _ in tqdm(range(num_tasks))]
    return results

def get_model(m_type: int) -> object:
    model = LinearRegression() if m_type == 0 else  RandomForestRegressor(n_estimators=random.randint(10, 30))
    return model

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default=0, type=int, choices=[0, 1], help="model type: 0 for default linear regression, 1 for RandormForestRegressor")
    parser.add_argument("-r", "--run", default="all", type=str, choices=["serial", "dist", "all"], help="Runs: only, serial, only distributed, or all")

    args = parser.parse_args()
    MODEL_TYPE = args.model
    RUN_TYPE = args.run 
    model_str = "LinearRegression" if MODEL_TYPE == 0 else "RandomForestRegressor"
    print(f"Selecting and training model type: {model_str}")
    
    X_train, X_test, y_train, y_test = prepare_data()
    run_times = {}

    if RUN_TYPE == "serial" or RUN_TYPE == "all":
        print("-----" * 10)
        print(f"\nSerially training {MAX_TASKS} models in {NUM_BATCHES} batches of size : {BATCH_SIZE} ... ")

        start_time = time.time()
        for tasks in range(NUM_BATCHES):
            # Fetch the model type
            lr_model =  get_model(MODEL_TYPE)
            score = run_serially(lr_model, X_train, X_test, y_train, y_test, BATCH_SIZE)
        end_time = time.time()
        run_times["serial"] = round((end_time - start_time), 2)
        print(f"Serially took: {run_times['serial']:.2f} seconds | mse: {score:.4f}")

    if RUN_TYPE == "dist" or RUN_TYPE == "all":
        # Put data in the object store
        # Fetch the model type
        lr_model =  get_model(MODEL_TYPE)
        lr_model_ref = ray.put(lr_model)
        x_train_ref  = ray.put(X_train)
        x_test_ref   = ray.put(X_test)
        y_train_ref  = ray.put(y_train)
        y_test_ref   = ray.put(y_test)

        print("-----" * 10)
        print(f"\nDistributed training {MAX_TASKS} models in {NUM_BATCHES} batches of size : {BATCH_SIZE} ... ")

        start_time = time.time()
        for tasks in range(NUM_BATCHES):
            results = run_distributed(lr_model_ref, x_train_ref, x_test_ref, y_train_ref, y_test_ref, BATCH_SIZE)
        dist_mse = ray.get(results[0])
        end_time = time.time()
        run_times["distributed"] = round((end_time - start_time), 2)
        print(f"Distributed took: {run_times['distributed']:.2f} seconds | mse: {dist_mse:.4f}")
        print("-----" * 10)
    pprint(run_times)
