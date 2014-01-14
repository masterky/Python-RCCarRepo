import wiringpi2, time


class LED(object):
	
	OUTPUT = 1
	DELAY_LED = 0.002
	status = False
	
	def __init__(self, pin):
		self.pin = pin
		wiringpi2.pinMode(self.pin,self.OUTPUT)
	def _write(self, status):
		if status:
			wiringpi2.digitalWrite(self.pin, 1)
			time.sleep(self.DELAY_LED)
		else: 
			wiringpi2.digitalWrite(self.pin, 0)
			time.sleep(self.DELAY_LED)
	def write(self):
		self.status = not(self.status)
		self._write(self.status)
	def reset(self):
		self._write(False)


class Servo(object):
	
	# Modes
	SOFT = 0
	HARD = 1
	
	# Var
	DELAY_PWM = 0.005
	HARD_PWM_OUTPUT = 2 # PWM Mode
	SOFT_PWM_OUTPUT = 1 # Output Mode
	def __init__(self, pin): 
		self.pin = pin
		self.mode = self.SOFT
		wiringpi2.pinMode(self.pin,self.SOFT_PWM_OUTPUT)
		wiringpi2.softPwmCreate(self.pin, 0, 100) # Whats with the reverse Direction?? 
	def __init__(self, pin=1):
		self.pin = 1
		self.mode = self.HARD
		wiringpi2.pinMode(self.pin,self.HARD_PWM_OUTPUT)
		
	def write(self, value):
		if self.mode is self.HARD:
			self._hardPwm(value)
		else: 
			self._softPwm(value)
	
	def _softPwm(self, value):
		wiringpi2.softPwmWrite(self.pin, value)
		time.sleep(self.DELAY_PWM)
		print "Write softPwm: ", value
	def _hardPwm(self, value):
		wiringpi2.pwmWrite(self.pin, value)
		time.sleep(self.DELAY_PWM)
		print "Write hardPwm: ", value
	def reset(self):
		wiringpi2.pinMode(self.pin, self.SOFT_PWM_OUTPUT)
		wiringpi2.digitalWrite(self.pin, 0)

#led = LED(13)
#led.write()
#led.reset()

#s = Servo(1)
#s.write(120)
#s.write(100)
#s.reset()
