import requests
import time
import json
from ray.job_submission import JobStatus


if __name__ == "__main__":

    # let's create a job submission request via HTTP
    # note that for this to run, you must have started
    # Ray on the local host: ray start --head
    resp = requests.post(
        "http://127.0.0.1:8265/api/jobs/",
        json = {
            "entrypoint": "python submit_job_example_1.py",
            "runtime_env": {},
            "job_id": None,
            "metadata": {"job_submission_id": "123"}
        }                 
    )
    rst = json.loads(resp.text)
    job_id = rst["job_id"]
    print(f"Ray submitted job id: {job_id}")

    # query the status
    start = time.time()
    while time.time() - start <= 60:
        resp = requests.get(
            f"http://127.0.0.1:8265/api/jobs/{job_id}"
        )
        rst = json.loads(resp.text)
        status = rst["status"]
        print(f"status: {status}")
        if status in {JobStatus.SUCCEEDED, JobStatus.STOPPED, JobStatus.FAILED}:
            break
        time.sleep(1)
    # query for logs
    resp = requests.get(
                f"http://127.0.0.1:8265/api/jobs/{job_id}/logs"
        )
    rst = json.loads(resp.text)
    logs = rst["logs"]
    print(logs)
    