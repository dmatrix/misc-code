import ray
#
# Create a Stateful Actor service that maintains state
# This service will be deployed onto one the ray worker in
# the cluster. It maintains the state in the object store shared
# by other workers
#


@ray.remote
class Counter(object):
    def __init__(self):
        self.value = 0

    def inc(self, inc_by=1):
        self.value = self.value + inc_by
        return self.value


if __name__ == "__main__":

    # Create an instance of an Actor. This returns an object reference
    counter = Counter.remote()
    inc_ref_1 = counter.inc.remote()
    print(f"inc_ref_1: {inc_ref_1}")
    inc_ref_2 = counter.inc.remote(2)
    print(f"inc_ref_2: {inc_ref_2}")

    # Fetch the values; notice it takes a list of object references
    # and iterates over each and returns a list
    result = ray.get([inc_ref_1, inc_ref_2])
    print(f"Incremented values: {result}")