#!/bin/sh

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