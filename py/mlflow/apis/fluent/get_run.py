#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#get_run
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Set existing run_ids
    run_ids = ["66f723d1f1664cd8aa9ae6920c1fdcb6", "4feca84314bc433bbcbd840a725f18c3"]

    # Get run info state for each run
    for run_id in run_ids:
        print("run_id: {}; lifecycle_stage: {}"
               .format(run_id, mlflow.get_run(run_id).info.lifecycle_stage))

