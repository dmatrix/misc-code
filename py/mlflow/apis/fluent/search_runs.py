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

    # Print pandas DataFrame's two rows and two columns
    print(df.iloc[:2, 0:1])

    print("-" * 35)

    # Search with order_by arguments
    df = mlflow.search_runs(order_by=["metrics.click_rate DESC"])

    # Print pandas DataFrame's two rows and one column
    print(df.loc[:2, ["metrics.click_rate"]])

    print("-" * 35)

    # Search using a filter_string with tag that has a case insensitive pattern
    filter_string = "tags.release.candidate ILIKE '%rc%'"
    df = mlflow.search_runs(["0"], filter_string=filter_string)

    # Print pandas DataFrame's two rows and one column
    print(df.loc[:2, ["tags.release.candidate"]])
