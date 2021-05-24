import pandas as pd


INGEST_DATA_REPO_PATHS = {
    'wine_set_path': "/Users/julesdamji/examples/py/delta-lake/winequality-red.csv"
}

if __name__ == "__main__":

    #
    # Read the data from a CSV file
    #
    wine_data_path = INGEST_DATA_REPO_PATHS.get('wine_set_path')
    wine_data = pd.read_csv(wine_data_path, delimiter=";")

    # Convert to Parquet DataFrames
    wine_data.to_parquet("/Users/julesdamji/examples/py/feature_store/data/wine_features.parquet")

    # Read the Parquet features back
    df = pd.read_parquet("../delta_to_feast/wine_features.parquet")
    print("Parquet DataFrame: {}".format("Wine data"))
    print("--")
    print(df)
