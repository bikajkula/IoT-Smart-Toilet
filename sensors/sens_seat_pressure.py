import paho.mqtt.client as mqtt

import firebase_admin

from firebase_admin import db

import time

import random

cred_object = firebase_admin.credentials.Certificate('cred.json ')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "dburl"
	})

address = ""	
ref = db.reference("/broker/")
ip = ref.get()

for k, v in ip.items():
	address = str(v)


broker_host = address  # Replace with the IP address or hostname of your MQTT broker
broker_port = 1883  # MQTT default port


# Create a MQTT client
publisher = mqtt.Client()

# Connect to the MQTT broker
publisher.connect(broker_host, broker_port)

ref = db.reference("/toilet/seat/")

def get_pressured_status():
	# Retrieve the seat pressured status from Firebase
	pressured_status = ref.child('pressured_status').get()
	return pressured_status

while True:
	# Publish a message to a topic
	
	is_pressured = get_pressured_status()
	
	publisher.publish("Kupatilo/solja/daska/pritisak", is_pressured)
	
	print(f"Toilet seat is pressured : {is_pressured}")
	
	time.sleep(5)

try:
    while True:
        pass
except KeyboardInterrupt:
    publisher.disconnect()
    publisher.loop_stop()
