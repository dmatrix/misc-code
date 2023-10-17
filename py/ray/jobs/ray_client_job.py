import ray

from submit_job_example_1 import task, launch_long_running_tasks, LaunchDistributedTasks

if __name__ == "__main__":

    # connect to the local cluster headnode
    # specify the runtime enviroment since we are importing 
    # functions from a local file. Workers will be started
    # in the /tmp/session. Read more here why you need this.
    # https://docs.ray.io/en/latest/cluster/running-applications/job-submission/ray-client.html#uploads
    ray.init("ray://127.0.0.1:10001",
             runtime_env={"working_dir":"."},
             )

    hdl = LaunchDistributedTasks.remote()
    print("Launched remote jobs")
    values = ray.get(ray.get(hdl.launch.remote()))
    print(f" list of results :{values}")
    print(f" Total results: {len(values)}")

