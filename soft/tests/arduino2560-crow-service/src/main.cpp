#include <asm/avr_arch.h>
#include <periph/map.h>
#include <Arduino.h>

#include <genos/ktimer.h>
#include <genos/schedee.h>
#include <genos/schedee_api.h>
#include <genos/coop_schedee.h>

#include <zillot/avr/usart.h>
#include <zillot/common/uartring.h>
#include <crow/tower.h>

#include <blink_task.h>
//#include <crow-service.h>
//#include <motors.h>

#define WITHOUT_COMMAND_TIMEOUT 300

AVR_USART_WITH_IRQS(usart0, USART0, USART0);
ZILLOT_UARTRING(serial0, usart0, 128, 16);

void commands_init();
int main()
{
	arch_init();
	genos::schedee_manager_init();
//	crow_services_init();

	irqs_enable();
    avr_usart_setup(USART0, 115200, 'n', 8, 1);
    serial0.begin();

	pinMode(13,1);
	pinMode(9,1);
	pinMode(10,1);

//	commands_init();
	blink_task_init();
//	motors_task_init();

	while(1)
		__schedule__();
}

void __schedule__()
{
	while (1)
	{
		//auto curtime = igris::millis();

		//crow::onestep();
		genos::ktimer_manager_step();
		genos::schedee_manager_step();
	}
}

void emergency_halt() 
{
	irqs_disable();
	while(1) {}
}

extern "C" int* __errno_location() 
{
	static int errno;
	return &errno;
}