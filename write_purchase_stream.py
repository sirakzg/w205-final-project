#!/usr/bin/env python
"""Extract purchase events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType


def purchase_event_schema():
    """
    root
    |-- event_type: string (nullable = false)
    |-- weapon_type: string (nullable = false)
    |-- user: string (nullable = false)
    |-- timestamp: string (nullable = true)
    """
    return StructType([
        StructField("event_type", StringType(), False),
        StructField("user", StringType(), False),
        StructField("weapon_type", StringType(), False),
    ])


@udf('boolean')
def is_purchase(event_as_json):
    """udf for filtering purchase events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase':
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
        .option("subscribe", "purchases") \
        .load()

    purchases = raw_events \
        .filter(is_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          purchase_event_schema()).alias('json')) \
        .select('json.*','timestamp')

    sink = purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_purchases") \
        .option("path", "/tmp/purchases") \
        .trigger(processingTime="30 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
