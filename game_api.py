#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request
from flask_api import status

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

@app.route("/purchase_a_sword")
def purchase_a_sword():
    if !request.is_json:
        return "Content not in JSON!",status.HTTP_400_BAD_REQUEST
    data = request.get_json()
    
    purchase_axe_event = {'event_type': 'purchase',
                          'type'      : 'sword',
                          'user'      : data['user']}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"


@app.route("/purchase_an_axe",methods = ['POST'])
def purchase_an_axe():
    if !request.is_json:
        return "Content not in JSON!",status.HTTP_400_BAD_REQUEST
    data = request.get_json()
    
    purchase_axe_event = {'event_type': 'purchase',
                          'type'      : 'axe',
                          'user'      : data['user']}
    log_to_kafka('events', purchase_axe_event)
    return "Axe Purchased!\n"
