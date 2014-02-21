import sys
import os
import pygame
from pygame.locals import * #import pygame libraries to gain control over your ps3 controller
import time
class stick(object):
	
	left_axe_right_left = 0
	left_axe_up_down = 0
	right_axe_right_left = 0
	right_axe_up_down = 0
	start_button = 0
	select_button = 0
	x_button = 0
	o_button = 0
	quad_button = 0
	triangle_button = 0
	steering_pad_right_left = 0
	steering_pad_up_down = 0
	left_up_button = 0
	left_down_button = 0
	right_up_button = 0
	right_down_button = 0
	left_axe_button = 0
	right_axe_button = 0
	mystick = None
	def __init__(self, MyStick):
		MyStick.init()
		self.mystick = MyStick
		if (self.load() != 2):
			self.findItAll()
			self.saveToFile()
		else:
			pass
	def pumpAxis(self, ID):
		return self.mystick.get_axis(ID)
	def pumpButton(self, ID):
		return self.mystick.get_button(ID)
	def pumpSteering(self, ID):
		return self.mystick.get_hat(0)[ID]
	def saveToFile(self):
		filename = self.mystick.get_name() + ".pygame_config"
		f = None
		try:
			f = open(filename)
			f.close()
			os.remove(filename)
			f = open(filename, 'w+')
			print "[StickClass] Old file was deleted, new file created"
		except IOError:
			f = open(filename, 'w+')
			print "[StickClass] [StickClass] New File was created"
			
		f.write('[Joystick]\n')
		f.write('[Config]\n')
		f.write('[' + self.mystick.get_name() + ']\n')
		f.write('left_axe_right_left=' + str(self.left_axe_right_left) + '\n')
		f.write('left_axe_up_down=' + str(self.left_axe_up_down) + '\n')
		f.write('right_axe_right_left=' + str(self.right_axe_right_left) + '\n')
		f.write('right_axe_up_down=' + str(self.right_axe_up_down) + '\n')
		f.write('start_button=' + str(self.start_button) + '\n')
		f.write('select_button=' + str(self.select_button) + '\n')
		f.write('x_button=' + str(self.x_button) + '\n')
		f.write('o_button=' + str(self.o_button) + '\n')
		f.write('quad_button=' + str(self.quad_button) + '\n')
		f.write('triangle_button=' + str(self.triangle_button) + '\n')
		f.write('steering_pad_right_left=' + str(self.steering_pad_right_left) + '\n')
		f.write('steering_pad_up_down=' + str(self.steering_pad_up_down) + '\n')
		f.write('left_up_button=' + str(self.left_up_button) + '\n')
		f.write('left_down_button=' + str(self.left_down_button) + '\n')
		f.write('right_up_button=' + str(self.right_up_button) + '\n')
		f.write('right_down_button=' + str(self.right_down_button) + '\n')
		f.write('left_axe_button=' + str(self.left_axe_button) + '\n')
		f.write('right_axe_button=' + str(self.right_axe_button) + '\n')
		f.write('[/Config]\n')
		f.write('[/Joystick]\n')
		pass
	def printInfo(self):
		print "[StickClass] ID:", self.mystick.get_id()
		print "[StickClass] Name:", self.mystick.get_name()
		print "[StickClass] Number of Buttons:", self.mystick.get_numbuttons()
		print "[StickClass] Number of Axes:", self.mystick.get_numaxes()
	def findAxe(self, stick):
		var = 0
		while 1:
			pygame.event.pump()
			for x in range(0, stick.get_numaxes()):
				var = (int) (stick.get_axis(x) * 10.0)
				if var != 0:
					return x
	def findButton(self,stick):
		var = 0
		while 1:
			pygame.event.pump()
			for x in range(0, stick.get_numbuttons()):
				if stick.get_button(x) is 1:
					return x
	def findHat(self, stick):
		var = 0
		while 1:
			pygame.event.pump()
			for x in range(0, stick.get_numhats()):
				hat = stick.get_hat(x)
				axe1 = hat[0];
				axe3 = hat[1]; 
				if axe1 is not 0:
					return 0
				if axe3 is not 0:
					return 1
	def load(self):
		
		filename = self.mystick.get_name() + ".pygame_config"
		try:
			f = open(filename, 'r')
			lines = f.readlines()
			if "[Config]" in lines[1] and "[/Config]" in lines[21]:
				left_axe_right_left = (int) (lines[3].split("=")[1].replace("\n", ""))
				left_axe_up_down = (int) (lines[4].split("=")[1].replace("\n", ""))
				right_axe_right_left = (int) (lines[5].split("=")[1].replace("\n", ""))
				
				if left_axe_right_left is 0 and left_axe_up_down is 0 and right_axe_right_left is 0:
					print "[StickClass] Invalid config file, wrong id selection"
					return 3
				
				self.right_axe_up_down = (int) (lines[6].split("=")[1].replace("\n", ""))
				self.start_button = (int) (lines[7].split("=")[1].replace("\n", ""))
				self.select_button = (int) (lines[8].split("=")[1].replace("\n", ""))
				self.x_button = (int) (lines[9].split("=")[1].replace("\n", ""))
				self.o_button = (int) (lines[10].split("=")[1].replace("\n", ""))
				self.quad_button = (int) (lines[11].split("=")[1].replace("\n", ""))
				self.triangle_button = (int) (lines[12].split("=")[1].replace("\n", ""))
				self.steering_pad_right_left = (int) (lines[13].split("=")[1].replace("\n", ""))
				self.steering_pad_up_down = (int) (lines[14].split("=")[1].replace("\n", ""))
				self.left_up_button = (int) (lines[15].split("=")[1].replace("\n", ""))
				self.left_down_button = (int) (lines[16].split("=")[1].replace("\n", ""))
				self.right_up_button = (int) (lines[17].split("=")[1].replace("\n", ""))
				self.right_down_button = (int) (lines[18].split("=")[1].replace("\n", ""))
				self.left_axe_button = (int) (lines[19].split("=")[1].replace("\n", ""))
				self.right_axe_button = (int) (lines[20].split("=")[1].replace("\n", ""))
				print "[StickClass] Config successfully loadad!"
				return 2
			else: 
				print "[StickClass] This is not a correct config file, exit"
				return 0
		except IOError:
			print "[StickClass] File doesnt exist"
			return 1
	def getStick(self):
		return self.mystick
	def findItAll(self):
		print "[StickClass] Please push the left axe right-left"
		time.sleep(3)
		self.left_axe_right_left = self.findAxe(self.mystick)
		print "[StickClass] Please push the left axe up-down"
		time.sleep(3)
		self.left_axe_up_down = self.findAxe(self.mystick)
		print "[StickClass] Please push the right axe right-left"
		time.sleep(3)
		self.right_axe_right_left = self.findAxe(self.mystick)
		print "[StickClass] Please push the right axe up-down"
		time.sleep(3)
		self.right_axe_up_down = self.findAxe(self.mystick)
		print "[StickClass] Please push the start button"
		time.sleep(3)
		self.start_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the select button"
		time.sleep(3)
		self.select_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the X button"
		time.sleep(3)
		self.x_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the O button"
		time.sleep(3)
		self.o_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the [] button"
		time.sleep(3)
		self.quad_button = self.findButton(self.mystick)
	
		print "[StickClass] Please push the triangle button"
		time.sleep(3)
		self.triangle_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the left axe button"
		time.sleep(3)
		self.left_axe_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the right axe button"
		time.sleep(3)
		self.right_axe_button = self.findButton(self.mystick)
		
		if (self.mystick.get_numhats() > 0):
			print "[StickClass] Please push the steering pad to the right"
			time.sleep(3)
			self.steering_pad_right_left = self.findHat(self.mystick)
			
			print "[StickClass] Please push the steering pad down"
			time.sleep(3)
			self.steering_pad_up_down = self.findHat(self.mystick)
			
		print "[StickClass] Please push the upper left up button"
		time.sleep(3)
		self.left_up_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the upper left down button"
		time.sleep(3)
		self.left_down_button = self.findButton(self.mystick)
	
		print "[StickClass] Please push the upper right up button"
		time.sleep(3)
		self.right_up_button = self.findButton(self.mystick)
		
		print "[StickClass] Please push the upper right down button"
		time.sleep(3)
		self.right_down_button = self.findButton(self.mystick)

#How to use this Class
#pygame.init()
#st = stick(pygame.joystick.Joystick(0))
#print "We are looking for something with an analog value, like a axe to control a rc-car"
#print st.findAxe(pygame.joystick.Joystick(0))
#print st.right_axe_button
#print st.left_down_button
