#!/usr/bin/env python
# -----------------------------------------------------------
# Extract join guild events from kafka and write them to hdfs
# Date: 4/12/2020
# Author: Jacky Ma & Sirak Ghebremusse
# -----------------------------------------------------------
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def guild_event_schema():
    """
    root
    |-- event_type: string (nullable = false)
    |-- guild_type: string (nullable = false)
    |-- user: string (nullable = false)
    |-- timestamp: string (nullable = true)
    """
    return StructType([
        StructField("event_type", StringType(), False),
        StructField("user", StringType(), True),
        StructField("guild_type", IntegerType(), True),
    ])


@udf('boolean')
def is_guild_event(event_as_json):
    """udf for filtering events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_guild':
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    #listening on guilds topic
    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "guilds") \
        .load()

    #only want to write event data and timestamp
    guilds = raw_events \
        .filter(is_guild_event(raw_events.value.cast('string'))) \
        .select(raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          guild_event_schema()).alias('json')) \
        .select('json.*','timestamp')

    #write to /tmp/guilds in hdfs every 30s
    sink = guilds \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guilds") \
        .option("path", "/tmp/guilds") \
        .trigger(processingTime="30 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
