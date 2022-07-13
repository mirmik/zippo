#include <asm/avr_arch.h>
#include <Arduino.h>
#include <string.h>

#include <genos/ktimer.h>
#include <genos/schedee.h>
#include <genos/schedee_api.h>
#include <genos/coop_schedee.h>

#include <crow/tower.h>
#include <crow/address.h>
#include <crow/nodes/publisher_node.h>
#include <crow/packet.h>

#include <igris/util/numconvert.h>
#include <zillot/avr/usart.h>
#include <zillot/avr/avr_i2c_device.h>

#include <ralgo/robo/motor.h>
#include <ralgo/filter/aperiodic_filter.h>

#include <blink_task.h>
#include <crow-service.h>
#include <motors.h>

#define WITHOUT_COMMAND_TIMEOUT 300

AVR_USART_WITH_IRQS(usart0, USART0, USART);

void commands_init();
int main()
{
	arch_init();
	genos::schedee_manager_init();

	irqs_enable();
    avr_usart_setup(USART0, 115200, 'n', 8, 1);
	crow_services_init();

	pinMode(13,1);
	pinMode(9,1);
	pinMode(10,1);

	commands_init();
	//blink_task_init();
	motors_task_init();

	while(1)
		__schedule__();
}

void __schedule__()
{
	while (1)
	{
		//auto curtime = igris::millis();

		crow::onestep();
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