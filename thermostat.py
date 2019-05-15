import sys
import time
from math import isnan
from LFSR import LFSRencrypt
import paho.mqtt.client as mqtt
import outdoor_temp
import window_mqtt
import serverManager
import threading
from flask import Flask
from flask import request
from flask import jsonify
import json

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

#Encrypted using LFSR
keys =LFSRencrypt()


#Initializing Devices
PORT_BUZZER = 2# D2
PORT_TEMP = 3#D3
PORT_BUTTON = 6# D6
PORT_ROTR = 0#A0

HVAC = ["AC","HEAT","WIND","FAN"]

grovepi.pinMode(PORT_BUZZER, "OUTPUT")
grovepi.pinMode(PORT_BUTTON, "INPUT")

#Functions to changed the desired Temperature
server = Flask('RPi Temperature Set Server')
def startup(default_temp):
    thread = threading.Thread(target=main,args=(default_temp,))
    thread.daemon = True
    thread.start()

@server.route('/send_temp',methods=['POST'])
def set_temp_callback():
    global set_temp
    payload = request.get_json()
    resp = server_manager.set_temp(payload)
    response = {'Response': resp[2],}
    if resp[0]==None and resp[1]==None:
        pass
    else:
        set_temp = resp[0]^keys[resp[1]]
    return json.dumps(response)

#Changs the current HVAC that will be displayed
def hvac(inTemp, outTemp,setTemp,currHVAC):
    global HVAC
    #5th line
    HVACidx = 3
    if inTemp == setTemp:#fan
        HVACidx= 3
    #1st line
    elif outTemp < inTemp and setTemp < inTemp:#WIND
        HVACidx=2
    #2nd line
    elif outTemp <= inTemp and setTemp > inTemp:#HEAT
        HVACidx=1
    #3rd line
    elif outTemp >= inTemp and setTemp < inTemp:#AC
        HVACidx=0
    elif outTemp > inTemp and setTemp > inTemp:#WIND
        HVACidx=2
    if(currHVAC!=HVACidx and currHVAC==2):
        client.publish("rpi-jj/home/windows","Exit Wind Mode: rpi-jj close")#exit window mode
    if(currHVAC!=2 and HVACidx ==2):
        client.publish("rpi-jj/home/windows","Entering Wind Mode: rpi-jj open")#enter window mode
    return HVACidx

#Prints to the LCD screen depending on the mode 
def display(inTemp, outTemp, setTemp,HVACset,windowMode):
    global HVAC 
    in_out=[setTemp,outTemp]
    mode = ['Desired: ','Outdoor: ']
    if(windowMode==0 or windowMode == 1):
        lcd.setText_norefresh("Temp: "+"{:>3}".format(inTemp)+"F  "+"{:>4}\n".format(HVAC[HVACset])+"{:>8} {:>3}F".format(mode[windowMode],in_out[windowMode]))
    else:
        lcd.setText_norefresh("Set Temp: "+"{:>3}F".format(setTemp))

#Main program loop
def main(default_temp):
    #display color and time
    lcd.setRGB(224,255,255)#cool blue color
    init_time = time.time()#get UTC time
    flag = True#flag for a while loop
    while(flag):
        [init_temp,hum] = grovepi.dht(PORT_TEMP,0)#get temp data
        time.sleep(.25)
        flag = False#if real data pre-set the flag to stop while loop
        if(isnan(init_temp)):#if NaN
            flag = True#set flag back to True
    global set_temp
    set_temp = default_temp
    init_temp = int(init_temp*9/5) + 32#convert temp to F
    windowMode = 0#default view
    outTemp = int(outdoor_temp.get_weather())
    HVACmode = hvac(init_temp,outTemp,set_temp,-1)
    screenFlag = True#prevents update of window mode if false
    counter = 0
    
    #Main while loop
    while(True):
        time.sleep(.25)
        grovepi.digitalWrite(PORT_BUZZER,0)#if buzzer was ringing then turn it off
        buttonRead = grovepi.digitalRead(PORT_BUTTON)#read port button
        new_temp = int(grovepi.analogRead(PORT_ROTR)/(1023/40))+60
        if(grovepi.digitalRead(PORT_BUTTON)):#while button is held down, loop
            init_time = time.time()#reset clock
            lcd.setRGB(224,255,255)#turn LCD on

        grovepi.digitalWrite(PORT_BUZZER,buttonRead)
        if(counter%2 == 0):
            [in_temp,hum] = grovepi.dht(PORT_TEMP,0)#get temp sensor data
            if(not isnan(in_temp)):
                in_temp = int(in_temp*9/5)+32
                init_temp = in_temp
        time.sleep(.25)
        counter+=1

        delta_time=time.time()-init_time#get current UTC time, to compare to initial time
        display(init_temp,outTemp,set_temp,HVACmode,windowMode)
        if(delta_time<5):#if less than 5 seconds have passed since turn on
            if(screenFlag):
                windowMode= (windowMode +buttonRead)%3#update window mode
                buttonRead = 0
            if(windowMode == 2):#if window mode is 2 then set temp must be available
                if(new_temp!=set_temp):
                    init_time = time.time()#if the rotarty is moved then reset the clock
                    set_temp=new_temp
            screenFlag = True#allows screen to be updated now
        else:
            lcd.setRGB(0,0,0)#turn off LCD
            screenFlag = False#prevents update once the button is pressed
        if(counter%2 == 0):
            HVACmode = hvac(init_temp,outTemp,set_temp,HVACmode)
        if(counter == 20):
            outTemp = int(outdoor_temp.get_weather())
            counter = 0
    return 0

if __name__ == '__main__':
    #Grabbing default temperature
    default_temp = 0;
    client = window_mqtt.mqtt_init()#initialize client
    try:
        ifile = open('default.txt', 'r')
        default_temp = int(ifile.read())
    except FileNotFoundError:
        default_temp = 70
    time.sleep(1)
    startup(default_temp)
    server_manager = serverManager.serverManager()
    server.run(debug=False,host = '0.0.0.0', port=4250)
    #Send new temperature to the default file
    ofile = open('default.txt','w')
    ofile.write(str(set_temp))
    ofile.close()
    lcd.setText_norefresh('')
    lcd.setRGB(0,0,0)
    print('')
