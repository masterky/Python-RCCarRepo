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
			wiringpi2.digitalWrite(1)
			time.sleep(DELAY_LED)
		else: 
			wiringpi2.digitalWrite(0)
			time.sleep(DELAY_LED)
	def write():
		self.status = !self.status
		_write(self.status)
	def reset():
		_write(False)


class Servo(object):
	
	# Modes
	SOFT = 0
	HARD = 1
	
	# Var
	DELAY_PWM = 0.005
	HARD_PWM_OUTPUT = 2
	SOFT_PWM_OUTPUT = 1
	def __init__(self, pin): 
		self.pin = pin
		self.mode = SOFT
		wiringpi2.pinMode(self.pin,self.SOFT_PWM_OUTPUT)
		wiringpi2.softPwmCreate(PIN_TO_PWM, 0, 100) # Whats with the reverse Direction?? 
	def __init__(self, pin=1):
		self.pin = 1
		self.mode = HARD
		wiringpi2.pinMode(self.pin,self.HARD_PWM_OUTPUT)
		
	def write(self, value):
		if self.mode == HARD:
			_hardPwm(value)
		else: 
			_softPwm(value)
	
	def _softServoPwm(self, value):
		# wiringpi2.softServoSettup()
		   #softServoWrite()
		pass
	
	def _softPwm(self, value):
		wiringpi2.softPwmWrite(self.pin, value)
		time.sleep(self.DELAY_PWM)
		print "Write softPwm: ", value
	def _hardpwm(self, value):
		wiringpi2.pwmWrite(self.pin, value)
		time.sleep(self.DELAY_PWM)
		print "Write hardPwm: ", value
	def reset(self):
		wiringpi2.pinMode(self.pin, SOFT_PWM_OUTPUT)
		wiringpi2.digitalWrite(self.pin, 0)

		
		
	
		