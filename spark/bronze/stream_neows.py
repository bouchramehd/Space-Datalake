from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, year, month, dayofmonth

KAFKA_BOOTSTRAP = "kafka:29092"
KAFKA_TOPIC = "nasa-neows"

BRONZE_PATH = "hdfs://namenode:9000/bronze/source=neows"
CHECKPOINT_PATH = "hdfs://namenode:9000/checkpoints/neows_bronze"

spark = (
    SparkSession.builder
    .appName("NASA-NeoWs-Bronze-Streaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("========================================")
print("NASA NeoWs -> Kafka -> Spark -> Bronze")
print("========================================")

# Read Kafka continuously
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "earliest")
    .load()
)

# Bronze = keep raw Kafka message
bronze_df = (
    kafka_df
    .select(
        col("key").cast("string").alias("kafka_key"),
        col("value").cast("string").alias("raw_json"),
        col("topic"),
        col("partition"),
        col("offset"),
        col("timestamp").alias("kafka_timestamp")
    )
    .withColumn("ingestion_timestamp", current_timestamp())
    .withColumn("year", year(col("ingestion_timestamp")))
    .withColumn("month", month(col("ingestion_timestamp")))
    .withColumn("day", dayofmonth(col("ingestion_timestamp")))
)

query = (
    bronze_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", BRONZE_PATH)
    .option("checkpointLocation", CHECKPOINT_PATH)
    .partitionBy("year", "month", "day")
    .trigger(processingTime="30 seconds")
    .start()
)

print("Streaming started.")
print(f"Kafka topic: {KAFKA_TOPIC}")
print(f"Bronze: {BRONZE_PATH}")

query.awaitTermination()