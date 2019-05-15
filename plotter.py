import sys
import time
import matplotlib.pyplot as plt
import numpy as npy


def hvac(inTemp, outTemp,setTemp):
    HVAC = ["AC","HEAT","WIND","FAN"]
    #5th line
    HVACidx = 0
    if inTemp == setTemp:#fan
        HVACidx= 0.5
    #1st line
    elif outTemp < inTemp and setTemp < inTemp:#WIND
        HVACidx=0.5
    #2nd line
    elif outTemp <= inTemp and setTemp > inTemp:#HEAT
        HVACidx=3.5
    #3rd line
    elif outTemp >= inTemp and setTemp < inTemp:#AC
        HVACidx=4.5
    elif outTemp > inTemp and setTemp > inTemp:#WIND
        HVACidx=0.5
    return HVACidx

if __name__ == '__main__':
	count = 0; 
	total_values = []
	indoor_temp = []
	outdoor_temp = []
	desired_temp = []

	total_cost = 0
	with open('data.csv','r') as f:
		for line in f:
			#grabs the temperature from each line
			total_values = line.split(',')
			indoor_temp.append(int(total_values[0]))
			outdoor_temp.append(int(total_values[1]))
			desired_temp.append(int(total_values[2]))
			HVAC_value = hvac(indoor_temp[count], outdoor_temp[count],desired_temp[count])
			total_cost+=HVAC_value
			count += 1

	print("For a cost of $.10 per kWh, the expected energy costs of our home is: $" + str(total_cost/10.0))

	fig = plt.figure("Energy Usage Estimator",figsize = (8,6))
	plt.plot(indoor_temp, label = 'Indoor Temp',marker = 's')
	plt.plot(outdoor_temp, label = 'Outdoor Temp',marker = 'o')
	plt.plot(desired_temp, label = 'Desired Temp', marker = 's')
	plt.title('Temperatures vs. Time')
	plt.xlabel('Time (hours)')
	plt.ylabel('Temperatures (F)')
	plt.legend(loc='lower right')
	plt.show()