# This is an example feature definition file

from google.protobuf.duration_pb2 import Duration

from feast import Entity, Feature, FeatureView, ValueType
from feast.data_source import FileSource

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
wine_features_table = FileSource(
    path="/Users/julesdamji/examples/py/delta-lake/wine_features.parquet",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

# Define an entity for the weather features. You can think of entity as a primary key used to
# fetch features.
acidity = Entity(name="fixed_acidity", value_type=ValueType.DOUBLE, description="acidity")

# Our parquet files contain serving data that includes four 10 columns. Here we define a Feature View that will allow us to serve this
# data to our model online.
wine_features_view = FeatureView(
    name="wine_features",
    entities=["fixed_acidity"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        Feature(name="volatile_acidity", dtype=ValueType.DOUBLE),
        Feature(name="citric_acid", dtype=ValueType.DOUBLE),
        Feature(name="residual_sugar", dtype=ValueType.DOUBLE),
        Feature(name="chlorides", dtype=ValueType.DOUBLE),
        Feature(name="pH", dtype=ValueType.DOUBLE),
        Feature(name="sulphates", dtype=ValueType.DOUBLE),
        Feature(name="alcohol", dtype=ValueType.DOUBLE),
        Feature(name="quality", dtype=ValueType.DOUBLE),
    ],
    online=True,
    input=wine_features_table,
    tags={},
)
