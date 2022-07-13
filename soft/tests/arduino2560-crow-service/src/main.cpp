#include <asm/avr_arch.h>
#include <periph/map.h>
#include <Arduino.h>

#include <genos/ktimer.h>
#include <genos/schedee.h>
#include <genos/schedee_api.h>
#include <genos/coop_schedee.h>
#include <genos/chardev.h>

#include <zillot/avr/usart.h>
#include <zillot/common/uartring.h>
#include <crow/tower.h>
#include <crow/nodes/service_node.h>
#include <crow/address.h>
#include <crow/gates/self_driven_gstuff.h>

#include <blink_task.h>
//#include <crow-service.h>
//#include <motors.h>

#define WITHOUT_COMMAND_TIMEOUT 300

AVR_USART_WITH_IRQS(usart0, USART0, USART0);
ZILLOT_UARTRING(serial0, usart0, 128, 16);
genos::zillot_chardev serial0_chardev(&serial0, "serial0");	

char send_buffer[100];
#define CROW_PACKET_SIZE 90

crow::hostaddr crowaddr = crow::address(".1.12.127.0.0.1:10009");
crow::service_node clinode;
crow::self_driven_gstuff crowgate;

genos::autom_schedee crow_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	while (serial0.avail())
	{
		char c;
		serial0_chardev.read(&c, 1);
		crowgate.newdata(c);
	}
	serial0_chardev.read(NULL, 0);
}, nullptr);

int crow_write_callback(void * priv, const char *data, unsigned int size)
{
	(void) priv;
	return serial0.write(data, size);
}

int crow_room_callback(void * priv)
{
	(void) priv;
	return serial0.room();
}

void crow_service_handle(char* a, int b, crow::service_node& c)
{
	c.reply("HelloWorld");
}

void crow_services_init()
{
	crowgate.init(
	    send_buffer,
	    crow_write_callback,
	    crow_room_callback,
	    NULL,
	    CROW_PACKET_SIZE);
	crowgate.bind(1);

	clinode.init(crow_service_handle);
	clinode.init_subscribe(crowaddr, CROWKER_SERVICE_BROCKER_NODE_NO, "zippo/ctr", 0, 0, 0, 0);
	clinode.bind(42);
	clinode.install_keepalive(2000);

	crow_schedee.start();
}


void commands_init();
int main()
{
	arch_init();
	genos::schedee_manager_init();

	irqs_enable();
    avr_usart_setup(USART0, 115200, 'n', 8, 1);
    serial0.begin();

	pinMode(13,1);
	pinMode(9,1);
	pinMode(10,1);

	blink_task_init();
	crow_services_init();

	while(1)
		__schedule__();
}

void __schedule__()
{
	while (1)
	{
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