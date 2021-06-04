"""
Some examples from https://sparkbyexamples.com/pyspark/pyspark-udf-user-defined-function/
"""
import pyspark
from pyspark.sql.functions import udf, col
import pyspark.sql.types as t


columns = ["Seqno", "Name"]
data = [(1, "jim jones"),
         (2, "jose gonzales"),
         (3, "julio cesar")]


def convert_case(name):
    return name.upper()


def length(name):
    return len(name)

@udf
def to_upper(s):
    if s is not None:
        return s.upper()


@udf(returnType=t.IntegerType())
def add_one(x):
    if x is not None:
        return x + 1


if __name__ == "__main__":
    spark = pyspark.sql.SparkSession.builder.appName("SimpleUDFs") \
        .getOrCreate()
    df = spark.createDataFrame(data=data, schema=columns)
    df.show()

    # Convert Python function to PySpark UDF
    pyspark_udf = udf(lambda s: convert_case(s), t.StringType())
    pyspark_len_udf = udf(lambda s: length(s), t.IntegerType())

    # Apply UDF to the DataFrame and add a column
    df2 = df.withColumn("Cureated Name", pyspark_udf(col('Name')))
    df2.show()
    df3 = df2.withColumn("Length", pyspark_len_udf(col('Name')))
    df3.show()

    # code from PySpark docs
    from pyspark.sql.types import IntegerType

    slen = udf(lambda s: len(s), IntegerType())

    df = spark.createDataFrame([(1, "John Doe", 21), (2, "Jane Doe", 22)], ("id", "name", "age"))
    df.show()
    df.select(slen("name").alias("slen(name)"), to_upper("name"), add_one("age")).show()


