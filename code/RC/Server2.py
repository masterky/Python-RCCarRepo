#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################
### Name: Server.py
### Author: Malte Koch
### exec: python server.py
### Version: 0.3
### Envirnoment: Python2.7
### Requiered Libraries: pygame (Download from: http://www.pygame.org) 
###                      wiringpi2 (Download from: https://github.com/WiringPi/WiringPi2-Python/)
### Operating System: Rasberry Pi or other Linux/GNU
#################################################

### Import Libraries
import socket
import time
from os import path
import sys
from datetime import datetime
import wiringpi2, time
from Servo import Servo, LED
import subprocess
import threading

# Pre Definded Var
PWM_MODE_MS = 0 #No Balancer enabled
NEUTRAL = 900
CLIENT_PORT = 5557

#WriringPi pins
THROTTLE_PIN = 1
STEERING_PIN = 0
FRONT_LIGHT_PIN = 2
BACK_LIGHT_PIN = 3

# IO Modes on Raspberry
OUTPUT = 1
INPUT = 0

print "[..] ", "Init Wiring Pi Lib"
wiringpi2.wiringPiSetup()

print "[..] ", "Init Servos"

throttle = Servo(THROTTLE_PIN)
steering = Servo(STEERING_PIN)

wiringpi2.pwmSetMode(PWM_MODE_MS)

print "[..] ", "Init LEDs"

frontLed = LED(FRONT_LIGHT_PIN)
backLed = LED(BACK_LIGHT_PIN)


### Open a Socket
s = socket.socket()
print "[..] New Socket on localhost:5556"
host = ''   # Get local machine name
port = 5556 # Reserve a port for your service.

 
### Bind the Socket
s.bind((host, port))        # Bind to the port
s.listen(0)  				# Now wait for client connection.
anz_diconnects = 0 			# MAX 5 Disconnects erlauben

def call(com):
	return subprocess.check_output(com).split("\n")[0]
def simpleCall(process):
	return subprocess.call(com)
def startWebcam():
	return simpleCall(["sudo", "sh", "/home/pi/MOTION/startMjpegStreamer.sh", "&"])
def stopWebcam():
	return simpleCall(["sh", "/home/pi/MOTION/killMjpegStreamer.sh", "&"])
def cleanUp():
	throttle.reset()
	steering.reset()
	frontLed.reset()
	backLed.reset()
	
try:
	### Begin the Loop
	while anz_diconnects is not 5:
		
		print '[..] Waiting for clients...'
		
		c, addr = s.accept()     # Establish connection with client
		print '[..] New Client: ', addr[0], ":", addr[1],":",  c
		print '[..] Connect to Client Socket'
		### Open a Socket
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		### Connect Socket to Client
		
		clientSocket.connect((addr[0], CLIENT_PORT))
		while True:			
			tStart = datetime.now()
			
			_buffer = bytearray(4)   # 4 zero bytes
			m = memoryview(_buffer)  # create the right buffer for the connection
			bytes_recv = c.recv_into(m)
			if (bytes_recv > 0):
				c1 = ord(m.tobytes()[0])
				c2 = ord(m.tobytes()[1])
				c3 = ord(m.tobytes()[2])
				c4 = ord(m.tobytes()[3])
				print "[..]", "Msg received: ", bytes_recv, c1 ,"," , c2,"," , c3 ,"," ,c4 # convert buffer back to int
				if c1 > 100: #forwards
					throttle.write(NEUTRAL + (c1 - 100) ) #takes about 0.005 Sec
					print "[..]", "THROTTLE : ", NEUTRAL + c1 - 100
				else:	#backwards
					throttle.write(NEUTRAL - c1)
					print "[..]", "THROTTLE : ", NEUTRAL - c1
				print "[..]", "ACTION : ", c4
				if c4 == 3:
					# change status
					frontLed.write()
				if c4 == 4:
					backLed.write()
				
				if c4 == 5:
					#get CPU temp
					temp = call(["vcgencmd", "measure_temp"])[5:7]
					clientSocket.send(chr(1) + chr(int(temp)))
				if c4 == 6:
					#start Webcam
					#not tested yet
					#startWebcam()			
					#stopWebcam()	

					
				
				
			else: 
				print "[..] Client Disconnected"
				c.close() # close Connection
				clientSocket.close()
				break
		anz_diconnects = anz_diconnects +1	
except (KeyboardInterrupt, SystemExit):
	print "[..] InteruptHandler is running!"
	print "[..] ", "All IO/s going to be reseted"
	cleanUp()
	s.close()
