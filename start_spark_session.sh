#!/bin/sh

echo "Starting the purchase spark session"
nohop docker-compose exec spark spark-submit /w205/w205-final-project/write_purchase_stream.py &


echo "Starting the user spark session"
nohop docker-compose exec spark spark-submit /w205/w205-final-project/write_user_stream.py &


echo "Starting the guild spark session"
nohop docker-compose exec spark spark-submit /w205/w205-final-project/write_guild_stream.py &

echo "Starting the record spark session"
nohop docker-compose exec spark spark-submit /w205/w205-final-project/write_player_record_stream.py &