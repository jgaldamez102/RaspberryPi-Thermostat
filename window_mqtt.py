import paho.mqtt.client as mqtt
import time

import sys

def on_connect(client, userdata, flags, rc):	
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def mqtt_init():#initialization function that 
    client = mqtt.Client()#create client
    client.on_message = on_message#assign on_message
    client.on_connect = on_connect#assign on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)#connect to this port
    client.loop_start()#start loop

    return client#return client to main code
