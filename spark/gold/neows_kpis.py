from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg,
    sum as spark_sum,
    when
)

spark = (
    SparkSession.builder
    .appName("NeoWs-Silver-to-Gold")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

SILVER_PATH = "hdfs://namenode:9000/silver/source=neows"
GOLD_BASE = "hdfs://namenode:9000/gold/source=neows"

print("=" * 60)
print("NASA NEOWS SILVER -> GOLD")
print("=" * 60)

df = spark.read.parquet(SILVER_PATH)

print("NeoWs Silver loaded.")

# ============================================================
# 1. GLOBAL KPIs
# ============================================================

global_kpis = df.agg(
    count("*").alias("total_asteroids"),
    spark_sum(
        when(col("potentially_hazardous") == True, 1).otherwise(0)
    ).alias("hazardous_asteroids"),
    avg("estimated_diameter_km").alias("avg_diameter_km"),
    avg("absolute_magnitude").alias("avg_absolute_magnitude")
)

global_kpis = global_kpis.withColumn(
    "hazardous_percentage",
    (col("hazardous_asteroids") / col("total_asteroids")) * 100
)

global_kpis.show(truncate=False)

(
    global_kpis.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/global_kpis")
)

# ============================================================
# 2. KPIs BY DATE
# ============================================================

by_date = (
    df
    .groupBy("event_date")
    .agg(
        count("*").alias("total_asteroids"),
        spark_sum(
            when(col("potentially_hazardous") == True, 1).otherwise(0)
        ).alias("hazardous_asteroids"),
        avg("estimated_diameter_km").alias("avg_diameter_km"),
        avg("absolute_magnitude").alias("avg_absolute_magnitude")
    )
    .withColumn(
        "hazardous_percentage",
        (col("hazardous_asteroids") / col("total_asteroids")) * 100
    )
    .orderBy("event_date")
)

by_date.show(truncate=False)

(
    by_date.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/by_date")
)

# ============================================================
# 3. HAZARD ANALYSIS
# ============================================================

hazard_analysis = (
    df
    .groupBy("potentially_hazardous")
    .agg(
        count("*").alias("asteroid_count"),
        avg("estimated_diameter_km").alias("avg_diameter_km"),
        avg("absolute_magnitude").alias("avg_absolute_magnitude")
    )
)

hazard_analysis.show(truncate=False)

(
    hazard_analysis.write
    .mode("overwrite")
    .parquet(f"{GOLD_BASE}/hazard_analysis")
)

print("=" * 60)
print("NEOWS GOLD COMPLETE")
print("=" * 60)

spark.stop()