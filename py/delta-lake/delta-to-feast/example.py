# This is an example feature definition file

from google.protobuf.duration_pb2 import Duration

from feast import Entity, Feature, FeatureView, ValueType
from feast.data_source import FileSource

# Read data from parquet files. Parquet is convenient for local development mode. For
# production, you can use your favorite DWH, such as BigQuery. See Feast documentation
# for more info.
serve_weather_features_table = FileSource(
    path="/Users/julesdamji/examples/py/delta-lake/delta-to-feast/data/serve_weather_forecast_features_parquet",
    event_timestamp_column="datetime",
    created_timestamp_column="created",
)

# Define an entity for the weather features. You can think of entity as a primary key used to
# fetch features.
yy_mm_dd = Entity(name="year_month_day", value_type=ValueType.STRING, description="Day, Month, Year")

# Our parquet files contain serving data that includes four 10 columns. Here we define a Feature View that will allow us to serve this
# data to our model online.
serve_weather_features_view = FeatureView(
    name="serve_weather_features",
    entities=["year_month_day"],
    ttl=Duration(seconds=86400 * 1),
    features=[
        Feature(name="temperature_00", dtype=ValueType.DOUBLE),
        Feature(name="wind_direction_00", dtype=ValueType.DOUBLE),
        Feature(name="wind_speed_00", dtype=ValueType.DOUBLE),
        Feature(name="temperature_08", dtype=ValueType.DOUBLE),
        Feature(name="wind_direction_08", dtype=ValueType.DOUBLE),
        Feature(name="wind_speed_08", dtype=ValueType.DOUBLE),
        Feature(name="temperature_16", dtype=ValueType.DOUBLE),
        Feature(name="wind_direction_16", dtype=ValueType.DOUBLE),
        Feature(name="wind_speed_16", dtype=ValueType.DOUBLE),
        Feature(name="power", dtype=ValueType.DOUBLE),
    ],
    online=True,
    input=serve_weather_features_table,
    tags={},
)
