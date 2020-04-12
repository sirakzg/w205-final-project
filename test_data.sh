#!/bin/bash
#title           :test_data.sh
#description     :This script will generate some test data
#author		 :Jacky Ma & Sirak Ghebremusse
#date            :4/12/2020
#version         :0.1
#usage		 :bash test_data.sh
#notes           :make sure API server is ready and hive tables are created


#create a test user
docker-compose exec mids ab -n 1 -T application/json -p /w205/w205-final-project/user_json.txt http://localhost:5000/create_user

#buy sword
docker-compose exec mids ab -n 1 -T application/json -p /w205/w205-final-project/user_json.txt http://localhost:5000/purchase_a_sword

#buy axe
docker-compose exec mids ab -n 1 -T application/json -p /w205/w205-final-project/user_json.txt http://localhost:5000/purchase_an_axe

#join guild
docker-compose exec mids ab -n 1 -T application/json -p /w205/w205-final-project/guild_json.txt http://localhost:5000/join_guild

#record death
docker-compose exec mids ab -n 1 -T application/json -p /w205/w205-final-project/record_json.txt http://localhost:5000/player_died