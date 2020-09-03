#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#list_run_info
#
import warnings
from pprint import pprint
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Get run info for experiment id 0, only include active runs
    pprint("RunInfo={}".format(mlflow.list_run_infos(str(0), run_view_type=1)))

    print("-" * 80)

    # Get run info for experiment id 0, include all runs
    # order_by valid types values are ['metric.key', 'parameter.key', 'tag.key', 'attribute.key']
    pprint("RunInfo={}".format(mlflow.list_run_infos(str(0), run_view_type=3,
                                                     order_by=["metric.metric_1 DESC"])))


