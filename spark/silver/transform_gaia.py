from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    DoubleType,
    StringType
)
from pyspark.sql.functions import col, current_timestamp

spark = (
    SparkSession.builder
    .appName("Gaia-Bronze-to-Silver")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

BRONZE_PATH = "hdfs://namenode:9000/bronze/source=gaia/year=2026/month=08/*.csv.gz"
SILVER_PATH = "hdfs://namenode:9000/silver/source=gaia"

print("=" * 60)
print("GAIA BRONZE -> SILVER")
print("=" * 60)

# Minimal schema for the columns we need
schema = StructType([
    StructField("source_id", LongType(), True),
    StructField("ra", DoubleType(), True),
    StructField("dec", DoubleType(), True),
    StructField("parallax", DoubleType(), True),
    StructField("pmra", DoubleType(), True),
    StructField("pmdec", DoubleType(), True),
    StructField("phot_g_mean_mag", DoubleType(), True),
    StructField("phot_bp_mean_mag", DoubleType(), True),
    StructField("phot_rp_mean_mag", DoubleType(), True),
    StructField("radial_velocity", DoubleType(), True),
])

print("Reading Gaia Bronze...")

df = (
    spark.read
    .option("header", "true")
    .schema(schema)
    .csv(BRONZE_PATH)
)

print("Bronze loaded.")

# Keep only valid essential rows
df = df.dropna(subset=["source_id", "ra", "dec"])

# Remove duplicate stars
df = df.dropDuplicates(["source_id"])

# Validate coordinates
df = df.filter(
    (col("ra") >= 0) &
    (col("ra") <= 360) &
    (col("dec") >= -90) &
    (col("dec") <= 90)
)

# Processing timestamp
df = df.withColumn(
    "silver_processed_at",
    current_timestamp()
)

print("Silver schema:")
df.printSchema()

print("Writing Silver Parquet...")

(
    df.write
    .mode("overwrite")
    .parquet(SILVER_PATH)
)

print("=" * 60)
print("GAIA SILVER COMPLETE")
print(SILVER_PATH)
print("=" * 60)

spark.stop()