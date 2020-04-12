#!/bin/sh

echo "Starting the purchase spark session"
docker-compose exec spark spark-submit /w205/w205-final-project/write_purchase_stream.py &

echo "Wait and starting the user spark session"
sleep 15
docker-compose exec spark spark-submit /w205/w205-final-project/write_user_stream.py &

sleep 15
echo "Wait and starting the guild spark session"
docker-compose exec spark spark-submit /w205/w205-final-project/write_guild_stream.py &

sleep 15
echo "Wait and starting the record spark session"
docker-compose exec spark spark-submit /w205/w205-final-project/write_player_record_stream.py &