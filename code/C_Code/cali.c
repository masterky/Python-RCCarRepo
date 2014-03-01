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
  //int l ;

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
  //pwmSetRange(200);
  printf("Starte Kalibrierung\n\r");
  printf("NEUTRAL!\n\r");
  pwmWrite (1, 900);
  delay(5000);
  printf("VOLLGAS!\n\r");
pwmWrite(1,1000);
delay(5000);
  printf("VOLLZURUECK!\n\r");
  pwmWrite(1, 800);
  delay(5000);
  printf("Kalibrierung beendet\n\r");
  delay (5000);
  return 0;
}
