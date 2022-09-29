#! /bin/env python3

# *** IMPORTS ***
import rainbowhat as rh
import paho.mqtt.client as mqtt
import time

# *** GLOBAL CONSTANTS ***
ECOST_TOPIC = "energy/electricity/dailycost"
GCOST_TOPIC = "energy/gas/dailycost"

# *** GLOBAL VARIABLES ***
global ecost = 0
global gcost = 0

# *** FUNCTION DEFINITIONS *** 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(ECOST_TOPIC,0),
                      (GCOST_TOPIC,0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global ecost
    global gcost
    if msg.topic == ECOST_TOPIC:
      ecost = float(msg.payload)
    elif msg.topic == GCOST_TOPIC:
      gcost = float(msg.payload)
    else:
      print("Unknown topic ", msg.topic)

# *** INITIAL SETUP ***
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("emonpi", "emonpimqtt2016")

client.connect("172.30.5.106", 1883, 60)
client.loop_start()

# *** MAIN LOOP ***
while True:
  print("Electricity:", ecost)
  print("Gas:", gcost)
  time.sleep(15)
  
