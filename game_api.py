#!/usr/bin/env python
# -----------------------------------------------------------
# a simple flask game API server that supports the following:
# create_user (post)
# purchase_a_sword(post)
# purchase_an_axe(post)
# join_guild(post)
# player_died(post)
#
# Author: Jacky Ma & Sirak Ghebremusse
# -----------------------------------------------------------
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


def log_to_kafka(topic, event):
    """logs the event to the input topic

    Parameter:
        topic (string): the topic to publish to
        event (dict): the json dictionary to be published

    Return:
        void
    """
    producer.send(topic, json.dumps(event).encode())


@app.route("/")
def default_response():
    """the default response
    get:
        response:
            200:
                "This is the default response!"
            400:
                Not supported method


    """
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

@app.route("/purchase_a_sword",methods = ['POST'])
def purchase_a_sword():
    """the purchase_a_sword request handler
    post:
        parameter:
            username: string (required)
        response:
            200:
                "Sword Purchased!"
            400:
                Not supported method
    """

    #require content type to be json
    if not request.is_json:
        return "Content not in JSON!\n",400
    data = request.get_json()
    #discard if no username
    if data is None or 'username' not in data or data['username'] == '':
        return "Missing User info!\n",400

    purchase_event = {
        'event_type' : 'purchase',
        'user'       : data['username'],
        'weapon_type': 'sword'
    }
    #log to kafka
    log_to_kafka('purchases', purchase_event)
    return "Sword Purchased!\n"


@app.route("/purchase_an_axe",methods = ['POST'])
def purchase_an_axe():
    """the purchase_an_axe request handler
    post:
        parameter:
            username: string (required)
        response:
            200:
                "Axe Purchased!"
            400:
                Not supported method
    """
    if not request.is_json:
        return "Content not in JSON!\n",400
    data = request.get_json()
    if data is None or 'username' not in data or data['username'] == '':
        return "Missing User info!\n",400

    purchase_event = {
        'event_type' : 'purchase',
        'user'       : data['username'],
        'weapon_type': 'axe'
    }
    log_to_kafka('purchases', purchase_event)
    return "Axe Purchased!\n"

@app.route("/create_user",methods = ['POST'])
def create_user():
    """the create user request handler
    post:
        parameter:
            username: string (required)
        response:
            200:
                "User Created!"
            400:
                Not supported method
    """
    if not request.is_json:
        return "Content not in JSON!\n",400
    data = request.get_json()
    if data is None or 'username' not in data or data['username'] == '':
        return "Missing User info!\n",400

    user_event = {
        'event_type': 'create_user',
        'user'      : data['username']
    }
    log_to_kafka('users', user_event)
    return "User created!\n"

@app.route("/join_guild",methods = ['POST'])
def join_guild():
    """the join_guild request handler
    post:
        parameter:
            username: string (required)
            guild_type: int (required)
        response:
            200:
                "Successfully joined guild!"
            400:
                Not supported method
    """
    if not request.is_json:
        return "Content not in JSON!\n",400
    data = request.get_json()
    if data is None or 'username' not in data or data['username'] == '':
        return "Missing User info!\n",400

    if 'guild_type' not in data or data['guild_type'] == '':
        return "Missing guild info!\n",400
    guild_event = {
        'event_type': 'join_guild',
        'user'      : data['username'],
        'guild_type': data['guild_type']
    }
    log_to_kafka('guilds', guild_event)
    return "Successfully joined guild!\n"

@app.route("/player_died",methods = ['POST'])
def player_died():
    """the join_guild request handler
   post:
       parameter:
           username   : string (required)
           guild_type : int (required)
           weapon_type: string (required)
           kills      : int (required)
           level      : int (required)
           gold       : int (required)
       response:
           200:
               "Recorded player death!"
           400:
               Not supported method
   """
    if not request.is_json:
        return "Content not in JSON!\n",400
    data = request.get_json()
    if data is None or 'username' not in data or data['username'] == '':
        return "Missing User info!\n",400

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
