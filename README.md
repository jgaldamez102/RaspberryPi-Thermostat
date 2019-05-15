# RaspberryPi-Thermostat

# EE250 Final Project - Thermostat    #
- **Name**: Joses Galdamez, Juan Vasquez-Sanchez 

***client_window_mqtt.py / window_mqtt.py*** - sets up the MQTT client/subscriber 
 	needed for sending the Window mode over. 

***thermostat.py*** - Main program

***outdoor_temp.py*** - RESTful API

***LFSR.py*** - handles the encryption for the HTTP request

***plotter.py / data.csv*** - extended program that calculates energy
 	costs based on the requirements. uses matplotlib

***serverManager.py / tempClient.py / tempServer.py*** - all set up the 
 	HTTP protocol that sends the appropriate temperature.
