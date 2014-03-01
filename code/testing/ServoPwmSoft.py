import wiringpi2, time
DELAY_PWM = 0.005
OUTPUT = 1
PIN_TO_PWM = 0
MIN = 2
MAX = 28
PWM_RANGE = 50
def softPwm():
	print "SoftPwm Mode"

	wiringpi2.wiringPiSetup()
	wiringpi2.pinMode(PIN_TO_PWM,OUTPUT)
	wiringpi2.softPwmCreate(PIN_TO_PWM,0,PWM_RANGE) # Setup PWM using Pin, Initial Value and Range parameters
	while True:
		
		for i in range(MIN, MAX):
			wiringpi2.softPwmWrite(PIN_TO_PWM, i) 	
			wiringpi2.delay(15)
			print "Write to PWM: ", i
		for i in reversed(range(MIN, MAX)):
			wiringpi2.softPwmWrite(PIN_TO_PWM, i) 	
			wiringpi2.delay(15)
			print "Write to PWM: ", i
def reset_pins(io):
	pins = [0,1,]
	for pin in pins:
		io.pinMode(pin,io.OUTPUT)
		io.digitalWrite(pin, io.LOW);
# direct
#io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
try:
    #reset_pins(io)   
    softPwm()

except (KeyboardInterrupt, SystemExit):
    reset_pins(io)
