#!/usr/bin/python

# Needed in Modules: 
# i2c-dev
# i2c-bcm2708

# Tools to install:
# apt-get i2c-tools
# apt-get python-smbus

# test: sudo i2cdetect -y 1

from Adafruit_PWM_Servo_Driver import PWM
import time

class AdafruitServoShield(object):
	
	# Address = 0x40-0x44
	def __init__(self, address):
		self.address = address
		self.driver = PWM(address, debug=False)
	
class AdafruitServo(AdafruitServoShield):
	
	pwmSleep = 0.0001 
	freq = 60 # 60 Hz std

	# Mostly servoMax = 600 for 4096, 150 MIN
	def __init__(self, address=0x41, channel=0, preset=True, servoMin=150, servoMax=650):
		AdafruitServoShield.__init__(self, address)
		self.preset = preset
		self.servoMin = servoMin
		self.servoMax = servoMax
		self.channel = channel
		self.driver.setPWMFreq(self.freq)
	def __setPWM__(self, value):
		print "Set PWM Adafruit Lib: ", value
		self.driver.setPWM(self.channel,0,value)
		time.sleep(self.pwmSleep)
 	def write(self, value=100, direction=0):
		_null = float(self.servoMax - self.servoMin)/2
		_middle = int(self.servoMin + _null)
		_range = self.servoMax - self.servoMin
		_x = float(_range) / float(200)
		value = value * _x
		value = int(value)
		 
		if (direction == 0):
			value = _middle + value
		else:
			value = _middle - value
		self.__setPWM__(value)

#servoMin = 150
#servoMax = 600
servo2 = AdafruitServo(channel=1, preset=True, servoMin=150, servoMax=650)
servo1 = AdafruitServo(channel=2, preset=True, servoMin=150, servoMax=650)





'''
while 1:
	for i in range(1,100):
		servo1.write(i, 1)
		#time.sleep(0.01)
		servo2.write(i, 1)
		time.sleep(0.001)
		print i
	for i in reversed(range(1, 100)):
		servo1.write(i, 1)
		#time.sleep(0.1)
		servo2.write(i, 1)
		time.sleep(0.001)
		print i
'''
