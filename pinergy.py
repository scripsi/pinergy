#! /bin/env python3

# *** IMPORTS ***
import rainbowhat as rh
import paho.mqtt.client as mqtt
import colorsys
import time
import math

# *** GLOBAL CONSTANTS ***
ECOST_TOPIC = "energy/electricity/dailycost"
GCOST_TOPIC = "energy/gas/dailycost"
EPOWER_TOPIC = "emon/emonpi/power1"
SHOW_GAS = 1
SHOW_ELECTRICITY = 2
SHOW_TOTAL = 3
RAINBOW_COLORS = [[0,255,0],
                  [0,255,0],
                  [255,128,0],
                  [255,128,0],
                  [255,128,0],
                  [255,0,0],
                  [255,0,0]]

# *** GLOBAL VARIABLES ***
ecost = 0
gcost = 0
tcost = 0
epower = 0
escale = 0
now_showing = SHOW_TOTAL
debug = False

# *** FUNCTION DEFINITIONS ***

# Update the 4 alphanumeric digit display
def update_display():
  if now_showing == SHOW_TOTAL:
    rh.display.clear()
    rh.display.print_number_str("{:.2f}".format(tcost/100))
  elif now_showing == SHOW_ELECTRICITY:
    rh.display.clear()
    rh.display.print_number_str("{:.2f}".format(ecost/100))
  elif now_showing == SHOW_GAS:
    rh.display.clear()
    rh.display.print_number_str("{:.2f}".format(gcost/100))

  rh.display.show()

# Update the 3 LEDs
def update_lights():
  if now_showing == SHOW_TOTAL:
    rh.lights.rgb(1,0,0)
  elif now_showing == SHOW_ELECTRICITY:
    rh.lights.rgb(0,1,0)
  elif now_showing == SHOW_GAS:
    rh.lights.rgb(0,0,1)

# Update the 7 Rainbow LEDs
def update_rainbow():
  p = max(escale,0)
  p = min(p,7)
  n = round(p)
  rh.rainbow.clear()
  for l in range(n):
    rh.rainbow.set_pixel(l,
                         RAINBOW_COLORS[l][0],
                         RAINBOW_COLORS[l][1],
                         RAINBOW_COLORS[l][2],
                         brightness=0.05)
  rh.rainbow.show()
      
@rh.touch.A.press()
def touch_a(channel):
  global now_showing
  now_showing = SHOW_TOTAL
  update_lights()
  update_display()

@rh.touch.B.press()
def touch_b(channel):
  global now_showing
  now_showing = SHOW_ELECTRICITY
  update_lights()
  update_display()

@rh.touch.C.press()
def touch_c(channel):
  global now_showing
  now_showing = SHOW_GAS
  update_lights()
  update_display()
   
# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqclient, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqclient.subscribe([(ECOST_TOPIC,0),
                        (GCOST_TOPIC,0),
                        (EPOWER_TOPIC,0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(mqclient, userdata, msg):
    global ecost, gcost, tcost, epower, escale
    if msg.topic == ECOST_TOPIC:
      ecost = float(msg.payload)
      tcost = gcost+ecost
      update_display()
    elif msg.topic == GCOST_TOPIC:
      gcost = float(msg.payload)
      tcost = gcost+ecost
      update_display()
    elif msg.topic == EPOWER_TOPIC:
      epower = int(msg.payload)
      escale = math.log1p((epower-100)/50)*1.4
      update_rainbow()
    else:
      print("Unknown topic ", msg.topic)

# *** INITIAL SETUP ***
update_display()
update_lights()
mq = mqtt.Client()
mq.on_connect = on_connect
mq.on_message = on_message
mq.username_pw_set("emonpi", "emonpimqtt2016")

mq.connect("172.30.5.106", 1883, 60)
mq.loop_start()

# *** MAIN LOOP ***
while True:
  if debug == True:
    print("Electricity:", ecost)
    print("Gas:", gcost)
    print("Total:", tcost)
    print("Power:", epower)
    print("Power Scale:", escale)
  time.sleep(5)
  
