import paho.mqtt.client as mqtt
import time

import sys

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("rpi-jj/home/windows")
    client.message_callback_add("rpi-jj/home/windows", window_on_message)

def window_on_message(client,userdata,msg):
    message = str(msg.payload, "utf-8")
    print(message)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def mqtt_init():#initialization function that 
    client = mqtt.Client()#create client
    client.on_message = on_message#assign on_message
    client.on_connect = on_connect#assign on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)#connect to this port
    client.loop_start()#start loop

    return client#return client to main code

if __name__ == '__main__':
	#this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
