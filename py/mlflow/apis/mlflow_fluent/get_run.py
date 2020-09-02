#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Set existing run_ids to delete
    run_ids = ["13ee9e661cbf4095a7c92cc55b4e12b4", "948fbf2d0b7f4056b3dd4914845a1e1b"]

    # Get run info for each runs
    [print("run_id={}; lifecycle_stage={}".format(run_id, mlflow.get_run(run_id).info.lifecycle_stage))
        for run_id in run_ids]

