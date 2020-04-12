#!/bin/sh
#title           :start_spark_session.sh
#description     :This script will start the 4 spark sessions that reads data off from kafka and writes to hive.
#author		 :Jacky Ma & Sirak Ghebremusse
#date            :4/12/2020
#version         :0.1
#usage		 :bash start_spark_session.sh
#notes           :run create_hive_table.sh and create_kafka_topic.sh and start API server before running this script

echo "Starting the purchase spark session"
nohup docker-compose exec spark spark-submit /w205/w205-final-project/write_purchase_stream.py > /dev/null 2>&1 &


echo "Starting the user spark session"
nohup docker-compose exec spark spark-submit /w205/w205-final-project/write_user_stream.py > /dev/null 2>&1 &


echo "Starting the guild spark session"
nohup docker-compose exec spark spark-submit /w205/w205-final-project/write_guild_stream.py > /dev/null 2>&1 &

echo "Starting the record spark session"
nohup docker-compose exec spark spark-submit /w205/w205-final-project/write_player_record_stream.py > /dev/null 2>&1 &