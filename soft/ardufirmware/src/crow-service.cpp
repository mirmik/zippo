#include <crow-service.h>
#include <crow/crow.h>
#include <crow/nodes/service_node.h>
#include <crow/gates/self_driven_gstuff.h>
#include <zillot/serial/uartring.h>
#include <zillot/serial/avr_usart_device.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>
#include <zillot/ioflags.h>
#include <crow/packet.h>

extern struct avr_usart_device_s usart0;
crow::hostaddr crowaddr = crow::address(".1.127.0.0.1:10009");

ZILLOT_DEF_UARTRING(serial0, &usart0.dev, 40, 40);

crow::self_driven_gstuff crowgate;
crow::service_node clinode;
autom_schedee crow_schedee;
char send_buffer[40];

#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 4
__attribute__((aligned(16)))
uint8_t crow_pool_buffer[CROW_PACKET_SIZE * CROW_PACKET_TOTAL];

void crow_schedee_thread(void * priv, int * state)
{
	(void) priv;
	(void) state;
	if (cdev_avail(&serial0.dev)) 
	{
		char c;
		cdev_read(&serial0.dev, &c, 1, 0);
		//debug_putchar(c);
		crowgate.newdata(c);
	}
	cdev_read(&serial0.dev, NULL, 0, IO_VIRTUAL_DISPLACE);
}

int crow_service_handle(char *, int, char * ans, int ansmax)
{
	(void) ansmax;
	sprintf(ans, "crow_service_handle");
	return 0;
}

int crow_write_callback(void * priv, const char *data, unsigned int size) 
{
	(void) priv;
	return cdev_write(&serial0.dev, data, size, IO_NOBLOCK);
}

void crow_services_init()
{
	crow::retransling_allowed = true;
	crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);

	crowgate.init(
		send_buffer, 
		crow_write_callback,
        NULL);
	crowgate.bind(1);

	uartring_install(&serial0, NULL);
	autom_schedee_init(&crow_schedee, crow_schedee_thread, NULL);
	schedee_start(&crow_schedee.sch);
	//clinode.init(crow_service_handle, 48);
	//clinode.bind(42);
}