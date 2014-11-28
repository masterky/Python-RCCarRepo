import wiringpi2, time

class AnalogReader(object):

        OUTPUT = 1
        status = False

        def __init__(self, pin):
                self.pin = pin
                wiringpi2.pinMode(self.pin,self.OUTPUT)
        def read(self):
               	return wiringpi2.analogRead(self.pin)
		

wiringpi2.wiringPiSetup()
#reader = AnalogReader(0)
wiringpi2.pinMode(0,1)
while 1:
	time.sleep(0.2)
	print wiringpi2.analogRead(0)
