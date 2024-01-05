import ray

@ray.remote
def get_node_list(start, end:int=5) -> list: 
    from random import randint
    return [randint(start, end) for _ in range(end)]

@ray.remote
def func_mult(num: int, mult:int=2) -> int:
    return num * mult

@ray.remote
def one() -> int:
    return 1

@ray.remote
def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    ray.init()

    # Executing using ray remote
    print("----- Executing using ray remote-----")
    id = ray.get(func_mult.remote(1, 2))
    print(id)
    node_list = ray.get(get_node_list.remote(5, 25))
    print(node_list)
    print("----- Executing using ray DAG-----")
    # Executing using ray DAG statically
    id_node_ref = func_mult.bind(1, 2)
    print(ray.get(id_node_ref.execute()))
    node_list_ref = get_node_list.bind(5, 25)
    print(ray.get(node_list_ref.execute()))

    dag = add.bind(100, one.bind())
    print(ray.get(dag.execute()))
    