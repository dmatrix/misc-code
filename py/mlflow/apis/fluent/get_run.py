#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Set existing run_ids
    run_ids = ["0709f1780b1e4cca8929c31fc53bcc5e", "406e594061b94a43881895cccce56b1f"]

    # Get run info state for each run
    for run_id in run_ids:
        (print("run_id={}; lifecycle_stage={}"
               .format(run_id, mlflow.get_run(run_id).info.lifecycle_stage)))

