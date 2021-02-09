import os
import multiprocessing as mp

import mlflow


def process_log_func(exp_name):
    import mlflow
    import random

    mlflow.set_experiment(exp_name)

    uri = mlflow.get_tracking_uri()
    mlflow.set_tracking_uri(uri)

    my_pid = os.getpid()
    parent_pid = os.getppid()
    artifact_path = "/tmp/features-" + str(my_pid) + ".txt"
    # create an artifact
    features = "rooms, zipcode, median_price, school_rating, transport"
    with open(artifact_path, 'w') as f:
        f.write(features)

    print("Running in PID: {}".format(my_pid))
    with mlflow.start_run():
        pid = "PID-" + str(my_pid)
        ppid = "PPID-" + str(parent_pid)
        mlflow.log_param(pid, my_pid)
        mlflow.log_param(ppid, parent_pid)
        mlflow.log_metric("metric", random.randint(1, 10))
        mlflow.log_artifact(artifact_path)

    experiment = mlflow.get_experiment_by_name(exp_name)
    if experiment:
        print("In pid: {}, experiment_id: {}".format(my_pid, experiment.experiment_id))


if __name__ == "__main__":
    experiment_name = "Test RayTune"
    cpus = mp.cpu_count()
    pid = os.getpid()

    mlflow.set_tracking_uri('sqlite:///mlruns.db')
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(experiment_id=mlflow.get_experiment_by_name(experiment_name).experiment_id):
        mlflow.log_param("driver-cpus", cpus)
        mlflow.log_param("driver_pid", pid)

    mp.set_start_method('fork', force=True)
    for _ in range(cpus * 2):
        process = mp.Process(target=process_log_func, args=[experiment_name])
        process.start()
        process.join()
