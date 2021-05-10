import pyspark
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import mlflow
import mlflow.pyspark.ml

if __name__ == '__main__':
    print("MLflow version: {}".format(mlflow.__version__))
    spark = pyspark.sql.SparkSession.builder.appName("BestParams") \
        .getOrCreate()
    dataset = spark.createDataFrame(
        [(Vectors.dense([0.0]), 0.0),
        (Vectors.dense([0.4]), 1.0),
         (Vectors.dense([0.5]), 0.0),
         (Vectors.dense([0.6]), 1.0),
         (Vectors.dense([1.0]), 1.0)] * 10,
        ["features", "label"])
    lr = LogisticRegression()
    grid = ParamGridBuilder().addGrid(lr.maxIter, [0, 1]).build()
    evaluator = BinaryClassificationEvaluator()
    cv = CrossValidator(estimator=lr, estimatorParamMaps=grid,
                        evaluator=evaluator,
                        parallelism=2)

    mlflow.pyspark.ml.autolog()
    cvModel = cv.fit(dataset)

    print("Average Metric: {}".format(cvModel.avgMetrics[0]))
    print("Number of folds: {}".format(cvModel.getNumFolds()))
    print("Best Model Coeff: {}".format(cvModel.bestModel.coefficients))
    print("Best Model Parameters: {}".format(cvModel.bestModel.params))

