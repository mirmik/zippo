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
#include <zillot/i2c/avr_i2c_device.h>
#include <zillot/serial/avr_usart_device.h>
#include <zillot/i2c/avr_i2c_device.h>

#include <ralgo/robo/motor.h>
#include <ralgo/filter/aperiodic_filter.h>

#include <blink_task.h>
#include <crow-service.h>
#include <motors.h>

#define WITHOUT_COMMAND_TIMEOUT 300

DECLARE_AVR_USART_WITH_IRQS(usart0, USART0, USART);


void commands_init();
int main()
{
	arch_init();
	genos::schedee_manager_init();
	ktimer_manager_init();
	crow_services_init();

	irqs_enable();
    avr_usart_setup(USART0, 115200, 'n', 8, 1);

	pinMode(13,1);
	pinMode(9,1);
	pinMode(10,1);

	commands_init();
	blink_task_init();
	motors_task_init();

	while(1)
		__schedule__();
}

void __schedule__()
{
	while (1)
	{
		auto curtime = millis();

		crow::onestep();
		ktimer_manager_step(curtime);
		genos::schedee_manager_step();
	}
}