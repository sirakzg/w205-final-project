#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

@app.route("/purchase_a_sword",methods = ['POST'])
def purchase_a_sword():
    if not request.is_json:
        return "Content not in JSON!",400
    data = request.get_json()
    if data['username'] == '':
        return "Missing User info!",400

    purchase_event = {
        'event_type' : 'purchase',
        'weapon_type': 'sword',
        'user'       : data['username']
    }
    log_to_kafka('purchases', purchase_event)
    return "Sword Purchased!\n"


@app.route("/purchase_an_axe",methods = ['POST'])
def purchase_an_axe():
    if not request.is_json:
        return "Content not in JSON!",400
    data = request.get_json()
    if data['username'] == '':
        return "Missing User info!",400

    purchase_event = {
        'event_type' : 'purchase',
        'weapon_type': 'axe',
        'user'       : data['username']
    }
    log_to_kafka('purchases', purchase_event)
    return "Axe Purchased!\n"

@app.route("/create_user",methods = ['POST'])
def create_user():
    if not request.is_json:
        return "Content not in JSON!",400
    data = request.get_json()
    if data['username'] == '':
        return "Missing User info!",400

    user_event = {
        'event_type': 'create_user',
        'user'      : data['username']
    }
    log_to_kafka('users', user_event)
    return "User created!\n"

@app.route("/join_guild",methods = ['POST'])
def join_guild():
    if not request.is_json:
        return "Content not in JSON!",400
    data = request.get_json()
    if data['username'] == '':
        return "Missing User info!",400

    guild_event = {
        'event_type': 'join_guild',
        'user'      : data['username'],
        'guild_type': data['guild_type']
    }
    log_to_kafka('guilds', guild_event)
    return "Successfully joined guild!\n"

@app.route("/player_died",methods = ['POST'])
def player_died():
    if not request.is_json:
        return "Content not in JSON!",400
    data = request.get_json()
    if data['username'] == '':
        return "Missing User info!",400

    died_event = {
        'event_type' : 'player_died',
        'user'       : data['username'],
        'guild_type' : data['guild_type'],
        'weapon_type': data['weapon_type'],
        'kills'      : data['num_kills'],
        'level'      : data['level'],
        'gold'       : data['gold']
    }
    log_to_kafka('records', died_event)
    return "Recorded player death!\n"
