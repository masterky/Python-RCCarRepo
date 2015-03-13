#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################
### Name: Client.py
### Author: Malte Koch
### exec: python client.py
### Version: 0.3
### Envirnoment: Python2.7
### Requiered Libraries: pygame (Download from: http://www.pygame.org)
### 					 xboxdrv
### For PS3 or XBox Controllers run:
###
### sudo xboxdrv --detach-kernel-driver
#################################################
### Operating System: Linux/GNU Version
#################################################

### Import Libraries
import time
import pygame
from stick import stick
from StickControl import StickControl
from datetime import datetime
from pygame.locals import * #import pygame libraries to gain control over your ps3 controller
import socket
import threading
from sys import exit
from os import popen
import select

# First Byte
SET_SPEED_FORWARD = 1;
SET_SPEED_REVERSE = 0;

# Secomd Byte					
SET_STEERING_LEFT = 1;
SET_STEERING_RIGHT = 0;

# Camera values
SET_CAMERA_NO_MOVE = -1
SET_CAMERA_RIGHT = 0
SET_CAMERA_LEFT = 1
SET_CAMERA_DOWN = 2
SET_CAMERA_UP = 3

# Third Byte, first 4 control bits
CLOSE_COMMUNICATION = 0;
SET_LIGHTS_ON = 1;
SET_CAMERA_ON = 2;
SET_CAMERA_ROTATION = 3;
SET_CAMERA_ROTATION_AUTO = 4;
SEARCH_FOR_GPS = 5;
MEASURE_CPU_TEMP = 6; 
MEASURE_VOLTAGE_ON_PI = 8; 

# Client specific
DO_NOTHING = 10
ACTIVATE = 1

### Open a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#REMOTE_HOST = '192.168.137.120' # Remote IP Address
REMOTE_HOST = '192.168.3.1'
#REMOTE_HOST = '10.42.0.3'
REMOTE_PORT = 5556  # Remote Port

### PS3 Controller Vars
IS_PS3_OR_XBOX_CONTROLLER = False
IS_INACCURACY_ENABLED = True

### Network Config
#IFACE = "wlan0"
IFACE = "wlp2s0"


def getSignalInDBm(essid):
	command = "iwlist " + IFACE +" scanning | grep " + essid  + " -B 2 | grep Signal | cut -d= -f3 | cut -d\" \" -f1"
	return popen(command).read().replace("\n","")
def getSignalQuality(essid):
	command = "iwlist " + IFACE + " scanning | grep " + essid + " -B 2 | grep Signal | cut -d= -f2 | cut -d\" \" -f1"
	return popen(command).read().replace("\n","")
def getConnectedTo():
	command = "iwconfig " + IFACE + " | grep ESSID | cut -d: -f2 | sed  's/\"//g'"
	return popen(command).read().replace("\n","")

def rcvThread():

	try:
		while True:
			try:
				_buffer = bytearray(2)   # 2 zero bytes
				m = memoryview(_buffer)  # create the right buffer for the connection
				bytes_recv = s.recv_into(m) #receiving 2 bytes
				# Buffer not zero
				if (bytes_recv == 2):
				# Check Whats the message about?
					c1 = ord(m.tobytes()[0])
					c2 = ord(m.tobytes()[1])
					print "[recv] Msg received : ", c1, " , ", c2
					if c1 == 1:
						#CPU Temperature
						print "Rasperry Pi CPU Temp: ", c2
					else:
						print "Could not Handle the message"
				else:
					pass
			except socket.error, e:
				time.sleep(0.5)
				print "[recv Thread] Wait for client connection to be astablished"

	except (KeyboardInterrupt, SystemExit):
		print "Exit thread"

### Connect Socket to remote Host
print '[..] Connecting to ', REMOTE_HOST, REMOTE_PORT
s.connect((REMOTE_HOST, REMOTE_PORT)) #connect to a remote host

# Create A Thread for Receiving messages
rvT = threading.Thread(target=rcvThread, args=(""))
rvT.daemon = True
rvT.start()	

### INIT VARIABLE ACTION_BYTE 1 to 4
ACTION_BYTE_1 = 0 # most sinificant bit, throttle direction (1 = forward, 0 = reverse) other least 7 bits = throttleData
ACTION_BYTE_2 = 0 # most sinificant bit, steering direction other least 7 bits = directionData
ACTION_BYTE_3 = 0 # action and actionData

### Init Control of the JoyStick
print "[..] Init Controller"

Control = StickControl()
try:
 	st = stick(Control.getStick(0))
except pygame.error, e:
	print "[Err] Controller not found"
	exit(0)

print "[..] New Controller found: ", Control.getStick(0).get_name()

if Control.getStick(0).get_name() == "Xbox Gamepad (userspace driver)":
	IS_PS3_OR_XBOX_CONTROLLER = True

### Make is Linux Check #####

# 
#

### Network init #####
'''
print "[..] Reading network information"
essid = getConnectedTo()
time.sleep(2)
print "[..] Connected to ", essid
print "[..] Signal Quality: ", getSignalQuality(essid), " (", getSignalInDBm(essid), " dB)"
print "\n"

## Wait a sec and start
print "[..] Init is over, lets play"
time.sleep(2)

'''

while 1:
	### Processing time without time.sleep(0.05) approx. 300 micro seconds 
	tStart = datetime.now()
	
	### Pump the Event 
	pygame.event.pump()
	
	### /-- Left Jojstick --/
	
	steering =  (int) (st.pumpAxis(st.left_axe_right_left) * 100.5)
	if IS_PS3_OR_XBOX_CONTROLLER and IS_INACCURACY_ENABLED:
		if steering < 8 and steering > -8:
			steering = 0
	if steering < 0:
		steering = - steering
		steeringDireciton = SET_STEERING_LEFT
	else:
		steeringDireciton = SET_STEERING_RIGHT
		
	###/-- Right Jojstick --/

	throttle = (int) (st.pumpAxis(st.right_axe_up_down) * 100.5)  #-1 = oben, +1 = unten
	if IS_PS3_OR_XBOX_CONTROLLER and IS_INACCURACY_ENABLED:
		if throttle < 5 and throttle > -5:
			throttle = 0
	
	if throttle < 0:
		# forward
		throttle = -throttle
		throttleDirection = SET_SPEED_FORWARD
	else:
		throttleDirection = SET_SPEED_REVERSE
		
	### Init Camera Steering
	cameraSteering = SET_CAMERA_NO_MOVE

	right_left_steering = st.pumpSteering(st.steering_pad_right_left)
	if (right_left_steering > 0):
		cameraSteering = SET_CAMERA_RIGHT #RIGHTcvc        
	if (right_left_steering < 0):
		cameraSteering = SET_CAMERA_LEFT #LEFT

	up_down_steering = st.pumpSteering(st.steering_pad_up_down)
	if (up_down_steering > 0):	
		cameraSteering = SET_CAMERA_UP #UP
	if (up_down_steering < 0):
		cameraSteering = SET_CAMERA_DOWN #DOWN
		
	### Analyse other buttons wheather pressed
	### Camera turning on after 5 sec

	actionData = ACTIVATE

	if (st.pumpButton(st.triangle_button) == 1):
		action = SET_LIGHTS_ON # Turn the lights on or whatever :)
	elif (st.pumpButton(st.right_up_button) == 1):
		action = MEASURE_CPU_TEMP
	elif (st.pumpButton(st.quad_button) == 1):
		action = SET_CAMERA_ON
	elif (st.pumpButton(st.left_up_button) == 1):
		action = MEASURE_VOLTAGE_ON_PI
	else:
		if (cameraSteering != SET_CAMERA_NO_MOVE):
			action = SET_CAMERA_ROTATION
			actionData = cameraSteering
		else: 
			action = DO_NOTHING

	### Set Action Bytes

	ACTION_BYTE_1 = ((throttleDirection << 7) | (throttle & 127))
	ACTION_BYTE_2 = ((steeringDireciton << 7) | (steering & 127))
	ACTION_BYTE_3 = ((action & 15) | (actionData << 4))

	
	### To not overstrain the Server, take a break and sleep :)
	time.sleep(0.07)
	
	### Merge Command
	command = chr(ACTION_BYTE_1) + chr(ACTION_BYTE_2) + chr(ACTION_BYTE_3)
	print "Throttle :", throttle , " , " , "Steering: ", steering
	### Send Command to RPi
	
	s.send(command)
	
	
	
	### Start Button ends the Program
	if st.pumpButton(st.start_button) is 1: 
		print "Goodbye"
		import sys
		sys.exit(0)
	
	### Calculate Processing Time
	tEnd = datetime.now()
	dif = tEnd - tStart
	
	### Print Action Bytes and dif Time
	# print "Command", ACTION_BYTE_1, "," , ACTION_BYTE_2, ", ", ACTION_BYTE_3, ", ", ACTION_BYTE_4
	# print "[TIME] ", dif.microseconds

