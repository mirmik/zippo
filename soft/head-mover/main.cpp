#include <hal/arch.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <igris/time/jiffies.h>

ISR(TIMER0_OVF_vect) 
{
	system_tick();
}

int main() 
{
//	arch_init();

	while(1) {}
}