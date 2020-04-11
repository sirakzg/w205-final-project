#!/usr/bin/env python
"""Extract user events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType


def user_event_schema():
    """
    root
    |-- event_type: string (nullable = true)
    |-- user: string (nullable = false)
    |-- timestamp: string (nullable = true)
    """
    return StructType([
        StructField("event_type", StringType(), False),
        StructField("user", StringType(), False),
    ])


@udf('boolean')
def is_create_user(event_as_json):
    """udf for filtering user events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'create_user':
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "users") \
        .load()

    user = raw_events \
        .filter(is_create_user(raw_events.value.cast('string'))) \
        .select(raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          user_event_schema()).alias('json')) \
        .select('json.*','timestamp')

    sink = user \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_create_user") \
        .option("path", "/tmp/users") \
        .trigger(processingTime="30 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
