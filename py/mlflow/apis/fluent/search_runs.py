#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#search_runs
#
import warnings
import mlflow

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    # Search with default arguments returning a pandas DataFrame
    df = mlflow.search_runs()
    print(df.iloc[:2, 0:3])

    print("-" * 70)

    # Search with order_by arguments
    df = mlflow.search_runs(order_by=["metrics.click_rate DESC"])
    print(df.loc[:2, ["metrics.click_rate", "run_id", "status"]])

    print("-" * 70)

    # Search using a filter_string with tag that has a case insensitive pattern
    filter_string = "tags.release.candidate ILIKE '%rc%'"
    df = mlflow.search_runs(filter_string=filter_string)
    print(df.loc[:2, ["tags.release.candidate", "run_id", "status"]])
