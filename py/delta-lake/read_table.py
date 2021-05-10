import pyspark

if __name__ == "__main__":
    spark = pyspark.sql.SparkSession.builder.appName("MyApp") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:0.8.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    df = spark.read.format("delta").load("five-delta-table")
    df.show()
