from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("TrafficAnalysis") \
    .getOrCreate()

# Define schema
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("vehicle_count", IntegerType(), True),
    StructField("average_speed", FloatType(), True),
    StructField("congestion_level", StringType(), True)
])

# Read streaming data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_data") \
    .option("startingOffsets", "latest") \
    .option("maxOffsetsPerTrigger", 1000) \
    .option("kafkaConsumer.pollTimeoutMs", 1000) \
    .option("failOnDataLoss", "false") \
    .load() 


# Convert value column to string and apply schema
traffic_df = df.selectExpr("CAST(value AS STRING) as value") \
    .selectExpr("from_json(value, 'sensor_id STRING, timestamp STRING, vehicle_count INT, average_speed FLOAT, congestion_level STRING') as data") \
    .select("data.*")

# Add watermark and process data with tumbling window
traffic_df_with_watermark = traffic_df \
    .withColumn("timestamp", col("timestamp").cast("timestamp")) \
    .withWatermark("timestamp", "2 minutes")  # Watermark: tolerate 2 minutes of late data

aggregated_df = traffic_df_with_watermark \
    .groupBy(col("sensor_id"), window(col("timestamp"), "2 minutes")) \
    .agg(avg("average_speed").alias("new_speed"))

# For simplicity, let's assume previous_speed_df comes from a batch source or a stateful operation
# Here we'll just proceed with the aggregation and filter logic
# Note: Joining with previous speeds in a streaming context may require stateful processing (e.g., using flatMapGroupsWithState)

# Write results back to Kafka (for now, just writing aggregated_df as an example)
query = aggregated_df \
    .selectExpr("CAST(sensor_id AS STRING) AS key", "to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "traffic_analysis") \
    .option("checkpointLocation", "checkpoint_dir") \
    .outputMode("append") \
    .start()

query.awaitTermination()