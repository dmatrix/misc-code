import pyspark
import pandas as pd


class Utils:
   @staticmethod
   def load_csv_data(path: str) -> pd.DataFrame:
      csv_df = pd.read_csv(path)
      csv_df.rename(columns={'Unnamed: 0': 'year_month_day'}, inplace=True)
      return csv_df

   @staticmethod
   def load_parquet_data(path: str) -> pd.DataFrame:
       parquet_df = pd.read_parquet(path)
       return parquet_df

   @staticmethod
   def create_spark_df(s: str, p_df: pd.DataFrame) -> pyspark.sql.DataFrame:
       return s.createDataFrame(p_df)

   @staticmethod
   def create_delta_table(data: pyspark.sql.DataFrame, feature_name: str) -> None:
       data.write.format("delta") \
           .mode("overwrite") \
           .save(feature_name)

   @staticmethod
   def save_data(data: str, fname: str, fmt: str) -> None:
       data.write\
           .format(fmt)\
           .mode("overwrite")\
           .save(fname)

   @staticmethod
   def read_data(source: str, fmt: str) -> pyspark.sql.DataFrame:
       return spark.read.format(fmt).load(t)



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


    # Convert to Spark DataFrames
    spark_weather_data = Utils.create_spark_df(spark, weather_data)
    spark_score_data = Utils.create_spark_df(spark, serve_data)
    
    # Create each dataframe as delta table feature set
    table_names = ["weather_forecast_features", "serve_weather_forecast_features"]
    parquet_files = ["weather_forecast_features_parquet", "serve_weather_forecast_features_parquet"]
    data_frames = [spark_weather_data, spark_score_data]
    [Utils.create_delta_table(f, t) for t, f in zip(table_names, data_frames)]

    # Read the table features back into a Spark DataFrame
    for t in table_names:
        df = Utils.read_data(t, "delta")
        print("Delta Table: {}".format(t))
        print("--")
        df.show(5)
        print(df.schema)

    # How to create Feast features from Delta Lake tables
    # TBD ...

    # Create parquet files
    [Utils.save_data(f, t, "parquet") for t, f in zip(parquet_files, data_frames)]

    # Read the Parquet features back into a Spark DataFrame
    for t in parquet_files:
        df = Utils.read_data(t, "parquet")
        print("Parquet DataFrame: {}".format(t))
        print("--")
        df.show(5)
        print(df.schema)








