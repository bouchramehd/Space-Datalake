from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp, to_date
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    DoubleType,
    BooleanType
)

spark = (
    SparkSession.builder
    .appName("NeoWs-Bronze-to-Silver")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

BRONZE_PATH = "hdfs://namenode:9000/bronze/source=neows"
SILVER_PATH = "hdfs://namenode:9000/silver/source=neows"

print("=" * 60)
print("NASA NEOWS BRONZE -> SILVER")
print("=" * 60)

json_schema = StructType([
    StructField("date", StringType(), True),
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("absolute_magnitude", DoubleType(), True),
    StructField("estimated_diameter_km", DoubleType(), True),
    StructField("potentially_hazardous", BooleanType(), True),
])

df = spark.read.parquet(BRONZE_PATH)

print("NeoWs Bronze loaded.")

df = df.withColumn(
    "json_data",
    from_json(col("raw_json"), json_schema)
)

df = df.select(
    col("json_data.id").alias("asteroid_id"),
    col("json_data.name").alias("asteroid_name"),
    to_date(col("json_data.date")).alias("event_date"),
    col("json_data.absolute_magnitude").alias("absolute_magnitude"),
    col("json_data.estimated_diameter_km").alias("estimated_diameter_km"),
    col("json_data.potentially_hazardous").alias("potentially_hazardous"),
    col("topic"),
    col("partition"),
    col("offset"),
    col("kafka_timestamp"),
    col("ingestion_timestamp")
)

# Nettoyage
df = df.dropna(subset=["asteroid_id"])

df = df.filter(
    col("estimated_diameter_km").isNull() |
    (col("estimated_diameter_km") >= 0)
)

df = df.dropDuplicates([
    "asteroid_id",
    "event_date"
])

df = df.withColumn(
    "silver_processed_at",
    current_timestamp()
)

print("Silver schema:")
df.printSchema()

print("Writing NeoWs Silver Parquet...")

(
    df.write
    .mode("overwrite")
    .parquet(SILVER_PATH)
)

print("=" * 60)
print("NEOWS SILVER COMPLETE")
print(f"Location: {SILVER_PATH}")
print("=" * 60)

spark.stop()