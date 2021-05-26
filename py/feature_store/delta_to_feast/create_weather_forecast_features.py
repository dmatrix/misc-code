import pyspark
from utils import Utils

INGEST_DATA_REPO_PATHS = {
    'weather_data_path': "https://raw.githubusercontent.com/dmatrix/olt-mlflow/master/model_registery/notebooks/data/windfarm_data.csv",
    'serve_data_path': "https://raw.githubusercontent.com/dmatrix/olt-mlflow/master/model_registery/notebooks/data/score_windfarm_data.csv"

}
if __name__ == "__main__":
    spark = pyspark.sql.SparkSession.builder.appName("DeltaLakeToFeast") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    #
    # Read the data from a CSV file
    #
    weather_data_path = INGEST_DATA_REPO_PATHS.get('weather_data_path')
    serve_data_path = INGEST_DATA_REPO_PATHS.get('serve_data_path')
    weather_data = Utils.load_csv_data(weather_data_path)
    serve_data = Utils.load_csv_data(serve_data_path)

    # Add datetime and created for the offline table for Feast to
    # ingest from and convert to Feast format
    weather_data = Utils.to_feast_fmt(weather_data)
    serve_data = Utils.to_feast_fmt(serve_data)

    # Convert to Spark DataFrames
    spark_weather_data = Utils.create_spark_df(spark, weather_data)
    spark_score_data = Utils.create_spark_df(spark, serve_data)

    # Create each dataframe as delta table feature set
    table_names = ["data/weather_forecast_features", "data/serve_weather_forecast_features"]
    parquet_files = ["data/weather_forecast_features_parquet", "data/serve_weather_forecast_features_parquet"]
    data_frames = [spark_weather_data, spark_score_data]
    [Utils.create_delta_table(f, t) for t, f in zip(table_names, data_frames)]

    # Read the Delta table features back into a Spark DataFrame
    for t in table_names:
        df = Utils.read_data(spark, t, "delta")
        print("Delta Table: {}".format(t))
        print("--")
        df.show(5)
        print(df.schema)

    # Create parquet files
    [Utils.save_data(f, t, "parquet") for t, f in zip(parquet_files, data_frames)]

    # Read the Parquet features back into a Spark DataFrame
    for t in parquet_files:
        df = Utils.read_data(spark, t, "parquet")
        print("Parquet DataFrame: {}".format(t))
        print("--")
        df.show(5)
        print(df.schema)