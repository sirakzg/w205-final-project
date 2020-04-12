#!/bin/sh

#title           :create_hive_table.sh
#description     :This script will create the 4 tables for our game data pipeline
#author		       :Jacky Ma & Sirak Ghebremusse
#date            :4/12/2020
#version         :0.1
#usage		       :bash create_hive_table.sh
#notes           :Wait until cloudera container is fully up"

#purchases:
echo "Creating the purchases table in hive."
docker-compose exec cloudera hive -e "create external table if not exists default.purchases (event_type string, user string, weapon_type string,  timestamp string) stored as parquet location '/tmp/purchases'  tblproperties ('parquet.compress'='SNAPPY');"

#user:
echo "Creating the users table in hive."
docker-compose exec cloudera hive -e "create external table if not exists default.users (event_type string, user string, timestamp string) stored as parquet location '/tmp/users'  tblproperties ('parquet.compress'='SNAPPY');"

#guild:
echo "Creating the guilds table in hive."
docker-compose exec cloudera hive -e "create external table if not exists default.guilds ( event_type string, user string, guild_type int,  timestamp string) stored as parquet location '/tmp/guilds'  tblproperties ('parquet.compress'='SNAPPY');"

#record:
echo "Creating the records table in hive."
docker-compose exec cloudera hive -e "create external table if not exists default.records (event_type string, user string, guild_type int, weapon_type string, kills int, level int, gold int, timestamp string) stored as parquet location '/tmp/records'  tblproperties ('parquet.compress'='SNAPPY');"

