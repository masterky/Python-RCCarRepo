/*
 * test2.c:
 *      Simple test program to test the wiringPi functions
 *      PWM test
 */
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main (void)
{
  int pin ;
  int l ;

  printf ("Raspberry Pi wiringPi PWM test program\n") ;

  if (wiringPiSetup () == -1)
    exit (1) ;

  for (pin = 0 ; pin < 8 ; ++pin)
  {
    pinMode (pin, OUTPUT) ;
    digitalWrite (pin, LOW) ;
  }
  //wmFrequency in Hz = 19.2e6 Hz / pwmClock / pwmRange
  pinMode (1, PWM_OUTPUT) ;
  //pwmSetClock(5);
  pwmSetMode(PWM_MODE_MS);//More realistic PWM, not balanced by internal balancer from broadcom  
  //pwmSetClock(4095);
  for (;;)
  {
	for (l = 900; l<1000; l++)
	{
	pwmWrite(1, l);
	delay(200);
	printf("Schreibe %d\r\n", l); 
	}
	
	for (l = 1000; l>800; l--)
        {
        pwmWrite(1, l);
        delay(200);
        printf("Schreibe %d\r\n", l);
        }
	for (l = 800; l<900; l++)
        {
        pwmWrite(1, l);
        delay(200);
        printf("Schreibe %d\r\n", l);
        }


 }
  return 0 ;
}
