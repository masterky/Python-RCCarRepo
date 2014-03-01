import wiringpi2, time
DELAY_PWM = 0.005
OUTPUT = 1
SET_PWM = 2
PIN_TO_PWM = 1
PWM_MODE_MS = 0 #No Balancer enabled
def softPwm():
	print "SoftPwm Mode"

	wiringpi2.wiringPiSetup()
	wiringpi2.pinMode(PIN_TO_PWM,SET_PWM)
	wiringpi2.pwmSetMode(PWM_MODE_MS)	
	#wiringpi2.softPwmCreate(PIN_TO_PWM,0,100) # Setup PWM using Pin, Initial Value and Range parameters
	#wiringpi2.softServoSettup()
	#softServoWrite()
	wiringpi2.pwmWrite(PIN_TO_PWM, 900) 	
	wiringpi2.delay(150)
	print "PWM is in NEUTRAL"
def reset_pins(io):
	pins = [0,1,]
	for pin in pins:
		io.pinMode(pin,io.OUTPUT)
		io.digitalWrite(pin, io.LOW);
# direct
#io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_SYS)
try:
    reset_pins(wiringpi2.GPIO())   
    #softPwm()

except (KeyboardInterrupt, SystemExit):
    reset_pins(io)
