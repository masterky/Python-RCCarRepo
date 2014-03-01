import wiringpi2, time
DELAY_PWM = 0.005
OUTPUT = 1
PIN_TO_PWM = 0

def softPwm():
	print "SoftPwm Mode"

	wiringpi2.wiringPiSetup()
	wiringpi2.pinMode(PIN_TO_PWM,OUTPUT)
	wiringpi2.softPwmCreate(PIN_TO_PWM,0,100) # Setup PWM using Pin, Initial Value and Range parameters

	for time in range(0,4):
        	for brightness in range(0,100): # Going from 0 to 100 will give us full off to full on
                	wiringpi2.softPwmWrite(PIN_TO_PWM,brightness) # Change PWM duty cycle
                	wiringpi2.delay(10) # Delay for 0.2 seconds
        	for brightness in reversed(range(0,100)):
                	wiringpi2.softPwmWrite(PIN_TO_PWM,brightness)
                	wiringpi2.delay(10)
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
