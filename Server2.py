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

# WiringPi Lib for GPIO
import wiringpi2

# Own classes for GPIO
from Servo import Servo, LED
from ServoShield import AdafruitServo
# Network connections
import socket

# Sys libs
from datetime import datetime
from os import path

import time
import sys
import subprocess
import threading

#paths
KILL_WEBCAM_SCRIPT = "/home/pi/pi2/Scripts/killMjpegStreamer.sh"
START_WEBCAM_SCRIPT = "/home/pi/pi2/Scripts/startMjpegStreamer.sh"


#first Byte
SET_SPEED_FORWARD = 1
SET_SPEED_REVERSE = 0

#secomd Byte					
SET_STEERING_LEFT = 1
SET_STEERING_RIGHT = 0

# Camera values
SET_CAMERA_NO_MOVE = -1
SET_CAMERA_RIGHT = 0
SET_CAMERA_LEFT = 1
SET_CAMERA_DOWN = 2
SET_CAMERA_UP = 3
					
# Third Byte, first 4 control bits
CLOSE_COMMUNICATION = 0
SET_LIGHTS_ON = 1
SET_CAMERA_ON = 2
SET_CAMERA_ROTATION = 3
SET_CAMERA_ROTATION_AUTO = 4
SEARCH_FOR_GPS = 5
MEASURE_CPU_TEMP = 6
MEASURE_VOLTAGE_ON_PI = 8
NOP = 10
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

#Camera status
cameraStatus = False

print "[..] ", "Init Wiring Pi Lib"
wiringpi2.wiringPiSetup()
wiringpi2.pwmSetMode(PWM_MODE_MS)

print "[..] ", "Init Servos"

throttleServo = Servo(THROTTLE_PIN)
steeringServo = AdafruitServo(address=0x41, channel=0, preset=True, servoMin=186, servoMax=686)
# Upwards dirction
cameraServo1  = AdafruitServo(address=0x41, channel=1, preset=True, servoMin=186, servoMax=686)
# left and right direction
cameraServo2 = AdafruitServo(address=0x41, channel=2, preset=True, servoMin=186, servoMax=686)

cameraServo1Value = 0
cameraServo1Direction = SET_CAMERA_LEFT
cameraServo2Value = 0
cameraServo2Direction = SET_CAMERA_UP

#for i in range(0,100):
#	steeringServo.write(value=i, direction=0)
#	time.sleep(0.1)
#for i in range(0,100):
#	time.sleep(0.1)
#	steeringServo.write(value=i, direction=1)

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

def shutdown():
	subprocess.call(["sudo", "shutdown", "-h", "now"])

def call(com):
	return subprocess.check_output(com).split("\n")[0]
def simpleCall(process):
	return subprocess.call(process)

# Yet to implement correctly

def startWebcamThread():
	subprocess.call(["sudo", "sh", START_WEBCAM_SCRIPT, "&"])	
def stopWebcamThread():
	subprocess.call(["sudo", "sh", KILL_WEBCAM_SCRIPT, "&"])
def getCPUTemp():
	return call(["vcgencmd", "measure_temp"])[5:7]
def startWebcam():
	t = threading.Thread(target=startWebcamThread, args=())
	t.daemon = True
	t.start()
	print "Setting camera status"
	return t
	#simpleCall(["sudo", "sh", "/home/pi/pi2/Scripts/startMjpegStreamer.sh", "&"])
def stopWebcam():
	print "Trying to stop webcam..."
	tstop = threading.Thread(target=stopWebcamThread, args=())
	tstop.daemon = True
	tstop.start()
	return tstop
	#simpleCall(["sudo", "sh", "/home/pi/pi2/Scripts/killMjpegStreamer.sh", "&"])

def setFlashLight(pin, status=True):
	pass
def cleanUp():
	throttleServo.reset()
	steeringServo.reset()
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
				print "[..] ", "steeringDirection ", steeringDirection
				print "[..]", "Action starts"
				print "[..]", "THROTTLE : ", throttle
				print "[..]", "Steering: ", steering
				# Write Throttle
				if (throttleDirection is SET_SPEED_FORWARD):
					print "[..] Drive forward: ", throttle
					#throttleServo.write(NEUTRAL + throttle) #takes about 0.005 Sec
				# Turn right	
				else:
					print "[..] Drive reverse: ", throttle
					#throttleServo.write(NEUTRAL - throttle) #takes about 0.005 Sec
				
				if (steeringDirection is SET_STEERING_LEFT):
					print "[..] Steering left: ", steering
					steeringServo.write(value=steering, direction=SET_STEERING_LEFT)
				else:
					print "[..] Steering right: ", steering
					steeringServo.write(value=steering, direction=SET_STEERING_RIGHT) 
				print "[..]", "ACTION : ", action
				if action == MEASURE_VOLTAGE_ON_PI:
					print "Measure Voltage"
				if action == MEASURE_CPU_TEMP:
					print "Measure CPU Temp"
					tmp = int(getCPUTemp())
					print "Temperature is ", tmp
					c.send(chr(1));
					c.send(chr(tmp)); 
				if action == 3:
					# change status
					frontLed.write()
				# Works fine :)
				if action == SET_CAMERA_ROTATION:
					print "Action camera rotation"
					CAMERA_INV = 20
					if actionData is SET_CAMERA_RIGHT:
						if cameraServo1Direction == SET_CAMERA_RIGHT:
                                                        cameraServo1Value = cameraServo1Value + CAMERA_INV
                                                        if (cameraServo1Value < 0):
                                                                cameraServo1Value=0
                                                                cameraServo1Direction = SET_CAMERA_LEFT
                                                        elif (cameraServo1Value >= 100):
                                                                cameraServo1Value = 100
                                                else:
							cameraServo1Value = cameraServo1Value - CAMERA_INV
                                                print "cameraServo2Value:", cameraServo2Value
                                                servo1Direction = 0
                                                if cameraServo1Direction == SET_CAMERA_RIGHT:
                                                        servo1Direction = 1
                                                cameraServo1.write(value=cameraServo1Value, direction=servo1Direction)
					elif actionData is SET_CAMERA_LEFT:
						if cameraServo1Direction == SET_CAMERA_LEFT:
                                                        cameraServo1Value = cameraServo1Value + CAMERA_INV
                                                        if (cameraServo1Value < 0):
                                                                cameraServo1Value=0
                                                                cameraServo1Direction = SET_CAMERA_RIGHT
                                                        elif (cameraServo1Value >= 100):
                                                                cameraServo1Value = 100
                                                else:
							cameraServo1Value = cameraServo1Value - CAMERA_INV
                                                print "cameraServo2Value:", cameraServo2Value
                                                servo1Direction = 0
                                                if cameraServo1Direction == SET_CAMERA_RIGHT:
                                                        servo1Direction = 1
                                                cameraServo1.write(value=cameraServo1Value, direction=servo1Direction)

					elif actionData is SET_CAMERA_UP:
						if cameraServo2Direction == SET_CAMERA_UP:
                                                        cameraServo2Value = cameraServo2Value + CAMERA_INV
                                                        if (cameraServo2Value < 0):
								cameraServo2Value=0
                                                                cameraServo2Direction = SET_CAMERA_DOWN
                                                        elif (cameraServo2Value >= 100):
                                                                cameraServo2Value = 100
                                                else:
                                                        cameraServo2Value = cameraServo2Value - CAMERA_INV
						print "cameraServo2Value:", cameraServo2Value
						servo2Direction = 0
						if cameraServo2Direction == SET_CAMERA_UP:
							servo2Direction = 1
                                                cameraServo2.write(value=cameraServo2Value, direction=servo2Direction)

					elif actionData is SET_CAMERA_DOWN:
						if cameraServo2Direction == SET_CAMERA_DOWN:
							cameraServo2Value = cameraServo2Value + CAMERA_INV
							if (cameraServo2Value < 0):
								cameraServo2Value = 0
								cameraServo2Direction = SET_CAMERA_UP
							elif (cameraServo2Value >= 100):
								cameraServo2Value = 100
						else:
							cameraServo2Value = cameraServo2Value - CAMERA_INV
						print "cameraServo2Value=", cameraServo2Value
						servo2Direction = 0
                                                if cameraServo2Direction == SET_CAMERA_UP:
                                                        servo2Direction = 1

						cameraServo2.write(value=cameraServo2Value, direction=servo2Direction)
						
				elif action==SET_CAMERA_ON:
					if actionData is 1:
						#Start Camera Stream
						if (cameraStatus is False):
							print "Starting Webcam now"
							cameraStatus = True
							startWebcam()
					else:
						#Stop Camera Stream
						if (cameraStatus):
							print "Stoping Webcam now"
							cameraStatus = False
							stopWebcam()
						else:
							pass
				
				elif action==CLOSE_COMMUNICATION:
					if actionData is 1:
						shutdown()
				# Actions starts here
				
				
				
			else: 
				print "[..] Client Disconnected"
				c.close() # close Connection
				break

except (KeyboardInterrupt, SystemExit):
	print "[..] InteruptHandler is running!"
	print "[..] ", "All IO/s going to be reseted"
	cleanUp()
	
