import logging
import time
import random
from typing import Tuple, List, Dict

import ray

class ActorCls:
    def __init__(self, name: str):
        self.name = name
        self.method_calls = {"method": 0}

    def method(self, **args) -> None:
        # Overwrite this method
        pass

    def get_all_method_calls(self) -> Tuple[str, Dict[str, int]]:
        return self.get_name(), self.method_calls
    
    def get_name(self) -> str:
        return self.name

@ray.remote
class ActorClsOne(ActorCls):
    def __init__(self, name: str):
        super().__init__(name)

    def method(self, **args) -> None:
        # do something with arg here
        # such as update DB specified in the arg
        time.sleep(args['timeout'])
        
        # update the respective counter
        self.method_calls["method"] += 1
    
@ray.remote
class ActorClsTwo(ActorCls):
    def __init__(self, name: str):
        super().__init__(name)

    def method(self, **args) -> None:
        # do something with arg here
        # such as update DB specified in the arg
        time.sleep(args['timeout'])
        
        # update the respective counter
        self.method_calls["method"] += 1

if __name__ == "__main__":
    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    CALLERS_NAMES = ["ActorClsOne", "ActorClsTwo"]
    CALLERS_CLS_DICT = {"ActorClsOne": ActorClsOne.remote("ActorClsOne"), 
                    "ActorClsTwo": ActorClsTwo.remote("ActorClsTwo")}
    count_dict = {"ActorClsOne": 0, "ActorClsTwo": 0}
    
    # Iterate over number of classes, and call randomly each super class Actor's 
    # method while keeping track locally here for verification.
    for _ in range(len(CALLERS_NAMES) * 3): 
        for _ in range(15):
            name = random.choice(CALLERS_NAMES)
            count_dict[name] += 1 
            CALLERS_CLS_DICT[name].method.remote(timeout=1, store="mongo_db") if name == "ActorClsOne" else CALLERS_CLS_DICT[name].method.remote(timeout=1.5, store="delta")
            
        print(f"State of counts in this execution: {count_dict}")
        time.sleep(0.5)

    # Fetch the count of all the methods called in each Actor called so far.
    print(ray.get([CALLERS_CLS_DICT[name].get_all_method_calls.remote() for name in CALLERS_NAMES]))