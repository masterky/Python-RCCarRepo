import RPi.GPIO as GPIO
from time import sleep
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)#GPIO OUT = P1 Pins


def setLED(pin, value):
	GPIO.output(pin, value)

while True:
	GPIO.output(23, True)
	print "LED"
	sleep(1)
	GPIO.output(23, False)
	print "LED AUS"
	sleep(1)
