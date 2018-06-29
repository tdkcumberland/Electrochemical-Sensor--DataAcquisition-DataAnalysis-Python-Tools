#SENSOR TEST SYSTEM CONTROLLER

#Python3 script to control a NumatoLab 2-relay module
#This script was specfically made to operate an air pump and a sample pump at fix intervals to creat reliable replication of each sensor test
#This script can be used within the BenchVue's TestFlow through a bash file or run independently

#Denpendency: pyserial. MUST be installed with for Python to have access to the COM ports

#Created by: Timothy Cumberland
#Email: tdkcumberland@gmail.com
#Last Eddited: June 21,2018

import serial
from time import sleep

portName = "COM2" #prior to running, check DeviceManager to confirm the port number
relayNum0 = 0
relayNum1 = 1
relayCmdon = "on"
relayCmdoff = "off"
#--Open port for communication--#
serPort = serial.Serial(portName, 19200, timeout=1)

#--Sending command to the the appropriate relay--#
#Turning air pump relay on
commandline = "relay "+ str(relayCmdon) +" "+ str(relayNum0) + "\n\r"
serPort.write(commandline.encode())

sleep(3) #wait for 3 seconds, can be adjusted

#turning sampling pump on
commandline = "relay "+ str(relayCmdon) +" "+ str(relayNum1) + "\n\r"
serPort.write(commandline.encode()) 

sleep(2) #wait for 2 seconds, can be adjusted, WARNING: leaving the sampling pump on for too long may damage the pump

#turn both pumps off
commandline = "relay "+ str(relayCmdoff) +" "+ str(relayNum0) + "\n\r"
serPort.write(commandline.encode())
commandline = "relay "+ str(relayCmdoff) +" "+ str(relayNum1) + "\n\r"
serPort.write(commandline.encode())

#--Close the port--#
serPort.close()
