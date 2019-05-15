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


1.	Introduction
For this project you will be implementing an IoT Thermostat. This thermostat behaves like a typical thermostat in that it will control your home’s heating and air-conditioning capabilities according to the desired temperature. However, in a step to achieve even greater energy savings, this thermostat has the added capability of opening/closing the windows in your home as well.

You will be building this thermostat to the specifications provided by the Design Team, found here in this document. This will require you to apply the skills you’ve developed in the labs for this course, so you should have everything you need to get started. There is also an opportunity to earn extra credit by furthering developing this product or by creating your own idea that applies the concepts covered in this course. 


3.	Hardware
To build the IoT Thermostat you’ll be using the following components:
	Raspberry Pi 3
	Grove Pi Shield
	LCD Screen
	Temperature & Humidity Sensor
Rotary Angle Sensor
	Buzzer
	Button

	


State Machine


The user switches between the views by pushing the button. When transitioning from the Edit View to the Default View, the desired temperature chosen by the user should be saved and backed up to a file. If the thermostat is restarted, the desired temperature should be restored.

Note: The thermostat should provide feedback to the user whenever the button is pushed by momentarily activating the buzzer.
Screen Saver
The LCD backlight should be active when the thermostat is being used. Any color is fine. However, after 5 seconds of inactivity (no physical user input), the backlight should be turned off.

Note: If the backlight is off, a button press should not change the current view. It should only turn on the backlight.
5.	Control Algorithm
Your thermostat will need to implement the logic described in this section for controlling the HVAC system. The mode should be updated as appropriate. The indoor temperature should be updated once per second. The outdoor temperature should be updated once every 10 seconds. The desired temperature is updated by the user. All temperature updates should be logged to console. The control logic should be activated whenever any temperature changes.


Relative to Indoor Temp.	
Outdoor Temp.	Desired Temp.	Mode
Lower	Lower	Wind (open windows)
Lower or Same	Higher	Heat
Higher or Same	Lower	AC
Higher	Higher	Wind (open windows)
*	Same	Fan
Table 1: HVAC Control Logic

When entering or leaving Wind mode, an MQTT message should be published using the format below in order to actuate the windows of your home. The topic and broker details are specified in the Configuration section.

Messages
Entering Wind mode: <hostname> open
Exiting Wind mode: <hostname> close

Replace <hostname> with the name of your Raspberry Pi.

Note: To ensure that your Control Algorithm works properly, you must implement a test mechanism that allows you to override one or more of the temperatures so that you can enter each mode. How you implement this is up to you (command-line argument, an HTTP request, etc.)
6.	Configuration
MQTT Broker: eclipse.usc.edu, port 11000
MQTT Window Topic: home/windows

Default Desired Temperature: 70 F (when no save file exists)

7.	Remote Control
Your IoT Thermostat wouldn’t be very “IoTy” unless you could control it remotely. Your thermostat should support setting the desired temperature through an HTTP request to your device on port 4250. The HTTP request should have the same configurable range as an input through the rotary angle sensor, i.e. [60, 100] F. An improper request should result in an appropriate error message being returned to the client.

Note: To protect your device from a hacker, you must implement some form of encryption in your HTTP request. The encryption should be implemented at the Application Layer, meaning you should be encrypting and decrypting the HTTP payload in your code. For this you may use one of the ciphers covered in lab, i.e. Caesar shift or Vigenère cipher, your own cipher, or a suitable library.

You must provide a sample client implementing this request. The user must be able to provide the desired temperature, through a command-line argument or stdin. 

8.	Energy Usage Estimator
A separate but bundled feature of your IoT Thermostat is its ability to estimate the energy consumption based on local weather and your usage habits. Create a script that takes as input a CSV (comma-separated values) file, plots the time series of temperatures, and outputs the expected energy costs when using the IoT Thermostat. 

Each line of the file contains the indoor temperature, the outdoor temperature, and the desired temperatures, in that order, separated by commas. An example of the file format is shown in the figure below.

72,77,70
71,77,70
71,76,70
70,74,70
70,74,70
70,75,72
Figure 6: Example of .csv file

You may assume that each line of the file represents a duration of one hour, meaning six hours have passed in the example file. Using matplotlib, create a line graph showing all three temperatures versus time. 

For each line of the file, you should apply the Control Algorithm logic described previously to determine what mode the IoT Thermostat would activate. Using this series of modes and the list of of energy costs shown in Table 2, your script should output the expected energy costs for your home.


Mode	Energy Usage (kWh)
AC	4.5
Heat	3.5
Wind	0.5
Fan	0.5
Table 2. HVAC Mode Energy Costs

The cost per kWh is $0.10.

As an example, the cost of the scenario depicted in Figure 6 is $1.50.
