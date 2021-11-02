#include <crow-service.h>
#include <crow/crow.h>
#include <crow/nodes/service_node.h>
#include <crow/gates/self_driven_gstuff.h>
#include <zillot/serial/uartring.h>
#include <zillot/serial/avr_usart_device.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>
#include <zillot/ioflags.h>

extern struct avr_usart_device_s usart0;
crow::hostaddr crowaddr = crow::address(".1.127.0.0.1:10009");

ZILLOT_DEF_UARTRING(serial0, &usart0.dev, 48, 16);

crow::self_driven_gstuff crowgate;
crow::service_node clinode;
autom_schedee crow_schedee;

void crow_schedee_thread(void *, int * state)
{	
	if (cdev_avail(&serial0.dev)) 
	{
		char buf[16];
		int len = cdev_read(&serial0.dev, buf, 16, 0);
		cdev_write(&serial0.dev, buf, len, 0);
	}

	//current_schedee_msleep(500);
	cdev_read(&serial0.dev, NULL, 0, IO_VIRTUAL_DISPLACE);
}

int crow_service_handle(char *, int, char * ans, int ansmax)
{
	sprintf(ans, "crow_service_handle");
	return 0;
}

void crow_services_init()
{
	uartring_install(&serial0, NULL);
	autom_schedee_init(&crow_schedee, crow_schedee_thread, NULL);
	schedee_start(&crow_schedee.sch);
	//crowgate.bind(1);
	//clinode.init(crow_service_handle, 48);
	//clinode.bind(42);
}