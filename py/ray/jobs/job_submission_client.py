from ray.job_submission import JobSubmissionClient, JobStatus
import time

def wait_until_status(job_id:str, status_to_wait_for:set, timeout_seconds:int=5):
    start = time.time()
    while time.time() - start <= timeout_seconds:
        status = client.get_job_status(job_id)
        print(f"status: {status}")
        if status in status_to_wait_for:
            break
        time.sleep(1)

if __name__ == "__main__":
    # If using a remote cluster, replace 127.0.0.1 with the head node's IP address.
    client = JobSubmissionClient("http://127.0.0.1:8265")
    job_id = client.submit_job(
        # Entrypoint shell command to execute
        entrypoint="python submit_job_example_1.py",
        # Path to the local directory that contains the script.py file
        runtime_env={"working_dir": "./"},
        metadata={"job_submission_id": "123", 
                  "submitter": "Jules Damji"}
    )
    print(job_id)

    # Loop until finished
    wait_until_status(job_id, {JobStatus.SUCCEEDED, 
                               JobStatus.STOPPED, 
                               JobStatus.FAILED}, 30)
logs = client.get_job_logs(job_id)
job_info = client.get_job_info(job_id)
print(f"Job Info: {job_info}")
print("----" * 10)
print(logs)
