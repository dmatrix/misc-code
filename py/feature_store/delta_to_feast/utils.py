import pandas as pd
import pyspark


class Utils:
    @staticmethod
    def load_csv_data(path: str) -> pd.DataFrame:
      csv_df = pd.read_csv(path)
      csv_df.rename(columns={'Unnamed: 0': 'year_month_day'}, inplace=True)
      return csv_df

    @staticmethod
    def to_feast_fmt(df: pd.DataFrame) -> pd.DataFrame:
        df['datetime'] = pd.to_datetime(df['year_month_day']).apply(lambda d: d.replace(tzinfo=None))
        df["created"] = pd.to_datetime(pd.Timestamp.now(tz=None).round("ms"))
        return df

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
    def save_data(data: pyspark.sql.DataFrame, fname: str, fmt: str) -> None:
       data.write\
           .format(fmt)\
           .mode("overwrite")\
           .save(fname)

    @staticmethod
    def read_data(spark: pyspark.sql.SparkSession, source: str, fmt: str) -> pyspark.sql.DataFrame:
       return spark.read.format(fmt).load(source)
