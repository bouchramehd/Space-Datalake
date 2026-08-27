from pyspark.sql import SparkSession
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

# Read Gaia ECSV
df = (
    spark.read
    .option("header", "true")
    .option("comment", "#")
    .option("inferSchema", "false")
    .csv(BRONZE_PATH)
)

print("Bronze loaded.")

# Select useful columns and cast types
df = df.select(
    col("source_id").cast("long").alias("source_id"),
    col("designation"),
    col("ra").cast("double").alias("ra"),
    col("dec").cast("double").alias("dec"),
    col("parallax").cast("double").alias("parallax"),
    col("pm").cast("double").alias("pm"),
    col("pmra").cast("double").alias("pmra"),
    col("pmdec").cast("double").alias("pmdec"),
    col("phot_g_mean_mag").cast("double").alias("phot_g_mean_mag"),
    col("phot_bp_mean_mag").cast("double").alias("phot_bp_mean_mag"),
    col("phot_rp_mean_mag").cast("double").alias("phot_rp_mean_mag"),
    col("bp_rp").cast("double").alias("bp_rp"),
    col("radial_velocity").cast("double").alias("radial_velocity"),
    col("ruwe").cast("double").alias("ruwe"),
    col("duplicated_source"),
    col("teff_gspphot").cast("double").alias("teff_gspphot"),
    col("logg_gspphot").cast("double").alias("logg_gspphot"),
    col("distance_gspphot").cast("double").alias("distance_gspphot")
)

# Essential values only
df = df.dropna(subset=["source_id", "ra", "dec"])

# Validate coordinates
df = df.filter(
    (col("ra") >= 0) &
    (col("ra") <= 360) &
    (col("dec") >= -90) &
    (col("dec") <= 90)
)

# Remove duplicated source IDs
df = df.dropDuplicates(["source_id"])

# Add processing timestamp
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
print(f"Location: {SILVER_PATH}")
print("=" * 60)

spark.stop()