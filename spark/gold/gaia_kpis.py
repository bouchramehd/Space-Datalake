from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg,
    when
)

spark = (
    SparkSession.builder
    .appName("Gaia-Silver-to-Gold")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

SILVER_PATH = "hdfs://namenode:9000/silver/source=gaia"
GOLD_BASE = "hdfs://namenode:9000/gold/source=gaia"

print("=" * 60)
print("GAIA SILVER -> GOLD")
print("=" * 60)

df = spark.read.parquet(SILVER_PATH)

print("Gaia Silver loaded.")

# ============================================================
# 1. GLOBAL KPIs
# ============================================================

global_kpis = df.agg(
    count("*").alias("total_stars"),
    avg("parallax").alias("avg_parallax"),
    avg("phot_g_mean_mag").alias("avg_g_magnitude"),
    avg("teff_gspphot").alias("avg_temperature"),
    avg("distance_gspphot").alias("avg_distance")
)

global_kpis.show(truncate=False)

(
    global_kpis.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/global_kpis")
)

# ============================================================
# 2. TEMPERATURE BANDS
# ============================================================

temperature_df = df.withColumn(
    "temperature_band",
    when(col("teff_gspphot").isNull(), "unknown")
    .when(col("teff_gspphot") < 3000, "<3000K")
    .when(col("teff_gspphot") < 4000, "3000-4000K")
    .when(col("teff_gspphot") < 5000, "4000-5000K")
    .when(col("teff_gspphot") < 6000, "5000-6000K")
    .when(col("teff_gspphot") < 7500, "6000-7500K")
    .otherwise(">=7500K")
)

temperature_gold = (
    temperature_df
    .groupBy("temperature_band")
    .agg(
        count("*").alias("star_count"),
        avg("distance_gspphot").alias("avg_distance"),
        avg("phot_g_mean_mag").alias("avg_g_magnitude"),
        avg("parallax").alias("avg_parallax")
    )
    .orderBy("temperature_band")
)

temperature_gold.show(truncate=False)

(
    temperature_gold.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/temperature_bands")
)

# ============================================================
# 3. MAGNITUDE BANDS
# ============================================================

magnitude_df = df.withColumn(
    "magnitude_band",
    when(col("phot_g_mean_mag").isNull(), "unknown")
    .when(col("phot_g_mean_mag") < 10, "<10")
    .when(col("phot_g_mean_mag") < 15, "10-15")
    .when(col("phot_g_mean_mag") < 18, "15-18")
    .when(col("phot_g_mean_mag") < 20, "18-20")
    .otherwise(">=20")
)

magnitude_gold = (
    magnitude_df
    .groupBy("magnitude_band")
    .agg(
        count("*").alias("star_count"),
        avg("parallax").alias("avg_parallax"),
        avg("distance_gspphot").alias("avg_distance"),
        avg("teff_gspphot").alias("avg_temperature")
    )
    .orderBy("magnitude_band")
)

magnitude_gold.show(truncate=False)

(
    magnitude_gold.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/magnitude_bands")
)

# ============================================================
# 4. DISTANCE BANDS
# ============================================================

distance_df = df.withColumn(
    "distance_band_pc",
    when(col("distance_gspphot").isNull(), "unknown")
    .when(col("distance_gspphot") < 100, "<100")
    .when(col("distance_gspphot") < 500, "100-500")
    .when(col("distance_gspphot") < 1000, "500-1000")
    .when(col("distance_gspphot") < 5000, "1000-5000")
    .otherwise(">=5000")
)

distance_gold = (
    distance_df
    .groupBy("distance_band_pc")
    .agg(
        count("*").alias("star_count"),
        avg("phot_g_mean_mag").alias("avg_g_magnitude"),
        avg("teff_gspphot").alias("avg_temperature"),
        avg("parallax").alias("avg_parallax")
    )
    .orderBy("distance_band_pc")
)

distance_gold.show(truncate=False)

(
    distance_gold.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/distance_bands")
)

print("=" * 60)
print("GAIA GOLD COMPLETE")
print("=" * 60)

spark.stop()