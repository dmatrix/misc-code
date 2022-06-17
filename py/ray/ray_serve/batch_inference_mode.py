from typing import List
import time

import numpy as np
import requests
from starlette.requests import Request

import ray
from ray import serve


@serve.deployment(route_prefix="/batch_compute")
class BatchCompute:

    @serve.batch(max_batch_size=5)
    async def handle_batch(self, numbers: List[int]):
        input_array = np.array(numbers)
        print(f"Our input array has shape: {input_array.shape}, value: {input_array.tolist()}")
        time.sleep(0.2)
        output_array = input_array * 20
        print(f"Our output array has shape: {output_array.shape}, value: {output_array.tolist()}")
        return output_array.astype(int).tolist()

    async def __call__(self, request: Request):
        return await self.handle_batch(int(request.query_params["number"]))


@ray.remote
def send_batch(number):
    resp = requests.get("http://localhost:8000/batch_compute?number={}".format(number))
    return int(resp.text)


if __name__ == '__main__':
    ray.init()
    serve.start()
    BatchCompute.deploy()

    # Let's use Ray to send all queries in parallel
    results_1 = ray.get([send_batch.remote(i) for i in range(25)])
    print("Result returned:", results_1)

    print("--" * 5)
    # Let's access via the Server Handle API
    serve_handle = BatchCompute.get_handle()
    results_2 = ray.get([serve_handle.handle_batch.remote(i) for i in range(25)])

    print("Result returned:", results_2)

    assert results_1 == results_2


