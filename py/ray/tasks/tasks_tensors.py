import logging
import random

from typing import Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import torch
import ray


def create_rand_tensor(size: Tuple[int, int]) -> torch.tensor:
    return torch.randn(size=(size), dtype=torch.float)


new_tensor=create_rand_tensor((2, 3))

@ray.remote
def transform_rand_tensor(tensor: torch.tensor) -> torch.tensor:
    return torch.transpose(tensor, 0, 1)

torch.manual_seed(42)
#
# Create a tensor of shape (X, 50)
#

tensor_list_obj_ref = [ray.put(create_rand_tensor(((i+1)*25, 150))) for i in range(0, 100)]

transformed_object_list = [transform_rand_tensor.remote(t_obj_ref) for t_obj_ref in tensor_list_obj_ref]
print(ray.get(transformed_object_list))