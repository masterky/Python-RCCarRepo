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

#first Byte
SET_SPEED_FORWARD = 1
SET_SPEED_REVERSE = 0

#secomd Byte					
SET_STEERING_LEFT = 1
SET_STEERING_RIGHT = 0
					
# Third Byte, first 4 control bits
CLOSE_COMMUNICATION = 0
SET_LIGHTS_ON = 1
SET_CAMERA_ON = 2
SET_CAMERA_ROTATION = 3
SET_CAMERA_ROTATION_AUTO = 4
SEARCH_FOR_GPS = 5
MEASURE_CPU_TEMP = 6
MEASURE_VOLTAGE_ON_PI = 8

# Pre Definded Var
PWM_MODE_MS = 0 #No Balancer enabled
NEUTRAL = 900

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
wiringpi2.pwmSetMode(PWM_MODE_MS)

print "[..] ", "Init Servos"

throttle = Servo(THROTTLE_PIN)
steering = Servo(STEERING_PIN)

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

def setFlashLight(pin, status=True):
	pass
def setFlashLight(pin, status=False):
	pass
def cleanUp():
	throttle.reset()
	steering.reset()
	frontLed.reset()
	backLed.reset()
	
try:
	### Begin the Loop
	while True:
		
		print '[..] Waiting for clients...'
		
		c, addr = s.accept()     # Establish connection with client
		print '[..] New Client: ', addr
		
		while True:
			
			tStart = datetime.now()
			
			_buffer = bytearray(4)   # 4 zero bytes
			m = memoryview(_buffer)  # create the right buffer for the connection
			try:
				bytes_recv = c.recv_into(m)
			except Exception, e:
				print "Client disconnected"
				break
				raise 
			if (bytes_recv > 0):
				
				c1 = ord(m.tobytes()[0])
				c2 = ord(m.tobytes()[1])
				c3 = ord(m.tobytes()[2])
				print "[..]", " Msg received: ", bytes_recv, c1 ,"," , c2, "," , c3
				
				#################################################
				# Shift incoming Data
				throttleDirection = (c1 >> 7)
				throttle = (c1 & 0x7f)
				steeringDirection = (c2 >> 7)
				steering = (c2 & 0x7f)
				action = (c3 & 0xF)
				actionData = (c3 >> 4)
				print "[..] ", "throttleDirection: ", throttleDirection , " , throttle: " , throttle, ", steeringDirection: ", steeringDirection, ", steering: ", steering, " , action: ", action, " , actionData: ", actionData
				print "[..]", "Action starts"
				print "[..]", "THROTTLE : ", throttle
				# Write Throttle
				if (throttleDirection is SET_SPEED_FORWARD):
					print "[..] Drive forward: ", throttle
					#throttle.write(NEUTRAL + throttle) #takes about 0.005 Sec
				# Turn right	
				else:
					print "[..] Drive reverse: ", throttle
					#throttle.write(NEUTRAL - throttle) #takes about 0.005 Sec
				print "[..]", "ACTION : ", action
				if action == 3:
					# change status
					frontLed.write()
				
				
				
				# Actions starts here
				
				
				
			else: 
				print "[..] Client Disconnected"
				c.close() # close Connection
				break

except (KeyboardInterrupt, SystemExit):
	print "[..] InteruptHandler is running!"
	print "[..] ", "All IO/s going to be reseted"
	cleanUp()
	
