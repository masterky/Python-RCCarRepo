import pygame
from stick import stick

from pygame.locals import * #import pygame libraries to gain control over your ps3 controller

class StickControl(object):
	def __init__(self):
		pygame.init()
	def getNumOfAvailSticks(self):
		return pygame.joystick.get_count()
	def getSticks(self):
		return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	def getStick(self, ID):
		return pygame.joystick.Joystick(ID)
	def getStickName(self, ID):
		return pygame.joystick.Joystick(ID).get_name()

#How to use this Class

#control = StickControl()
#print control.getNumOfAvailSticks()
#print control.getStickName(0)

