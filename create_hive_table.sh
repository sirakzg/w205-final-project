#!/bin/sh

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

