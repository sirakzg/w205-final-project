#!/bin/sh
#title           :create_kafka_topic.sh
#description     :This script will create the 5 topics for our game data pipeline
#author		       :Jacky Ma & Sirak Ghebremusse
#date            :4/12/2020
#version         :0.1
#usage		       :bash create_kafka_topic.sh
#notes           :Wait until kafka broker is up, use "docker-compose exec kafka cub kafka-ready -b kafka:29092 1 20"

echo "Creating the events topic in kafka"
docker-compose exec kafka kafka-topics --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

echo "Creating the events topic in purchases"
docker-compose exec kafka kafka-topics --create --topic purchases --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

echo "Creating the events topic in users"
docker-compose exec kafka kafka-topics --create --topic users --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

echo "Creating the events topic in guilds"
docker-compose exec kafka kafka-topics --create --topic guilds --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181

echo "Creating the events topic in records"
docker-compose exec kafka kafka-topics --create --topic records --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:32181