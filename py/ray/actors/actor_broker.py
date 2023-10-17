from typing import Dict, Any
import ray

def compute_cube(x: int) -> int:
        return x * x * x

@ray.remote
def run_tasks(args: Dict[str, Any]):
    func = args['func']
    data = args['data']
    result = func(data)
    return result

@ray.remote
class BrokerActor():
    def __init__(self):
        self.id_to_ref = {}

    @ray.method(num_returns=2)
    def exec(self, task_args) -> object:
        ray_task = task_args['ray_func']
        ref = ray_task.remote(task_args)
        val = ray.get(ref)
        self.id_to_ref[ref.hex()] = ref
        return (val, ref.hex())
    
    def get_ref(self, id) -> object:
        return self.id_to_ref[id]
    
if __name__ == "__main__":
    broker = BrokerActor.options(
        namespace="broker",
        name="actor",
        lifetime="detached").remote()
    
    func_args = {'func': compute_cube,
                 'data': 3,
                 'ray_func': run_tasks}
    
    val, id = ray.get(broker.exec.remote(func_args))
    task_ref = ray.get(broker.get_ref.remote(id) )
    print(f"Broker executed returned func value:{val} ")
    print(f"Broker reference id :{id} ")
    print(f"Broker function ref: {task_ref} for id :{id} ")

    


