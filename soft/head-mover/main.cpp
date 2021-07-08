#include <hal/arch.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <genos/jiffies.h>
#include <periph/map.h>

#include <drivers/gpio/avr_gpio.h>

ISR(TIMER0_OVF_vect) 
{
	system_tick();
}

genos::avr_gpio gpio(GPIOB);

int main() 
{
	

	while(1) {}
}