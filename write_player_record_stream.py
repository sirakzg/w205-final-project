#!/usr/bin/env python
# -----------------------------------------------------------
# Extract player death events from kafka and write them to hdfs
# Date: 4/12/2020
# Author: Jacky Ma & Sirak Ghebremusse
# -----------------------------------------------------------
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType,IntegerType


def player_death_event_schema():
    """
    root
    |-- event_type: string (nullable = false)
    |-- user: string (nullable = false)
    |-- guild_type: int (nullable = false)
    |-- weapon_type: string (nullable = false)
    |-- kills: int (nullable = false)
    |-- level: int (nullable = false)
    |-- gold: int (nullable = false)
    |-- timestamp: string (nullable = true)
    """
    return StructType([
        StructField("event_type", StringType(), False),
        StructField("user", StringType(), False),
        StructField("guild_type", IntegerType(), False),
        StructField("weapon_type", StringType(), False),
        StructField("kills", IntegerType(), False),
        StructField("level", IntegerType(), False),
        StructField("gold", IntegerType(), False),
    ])


@udf('boolean')
def is_player_death(event_as_json):
    """udf for filtering purchase events
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'player_died':
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    #listening on records topic
    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "records") \
        .load()

    #only want the event data and timestamp
    death = raw_events \
        .filter(is_player_death(raw_events.value.cast('string'))) \
        .select(raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          player_death_event_schema()).alias('json')) \
        .select('json.*','timestamp')

    #30 sec batch job
    sink = death \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_records") \
        .option("path", "/tmp/records") \
        .trigger(processingTime="30 seconds") \
        .start()

    sink.awaitTermination()


if __name__ == "__main__":
    main()
