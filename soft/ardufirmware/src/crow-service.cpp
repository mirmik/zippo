#include <crow-service.h>
#include <crow/nodes/nospublisher.h>
#include <crow/crow.h>
#include <crow/constexpr_hexer.h>
#include <crow/nodes/service_node.h>
#include <crow/gates/self_driven_gstuff.h>
#include <zillot/common/uartring.h>
#include <zillot/avr/usart.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>
#include <genos/chardev.h>
#include <zillot/ioflags.h>
#include <command.h>
#include <crow/packet.h>

extern zillot::avr::usart usart0;
ZILLOT_UARTRING(serial0, usart0, 100, 16);
genos::zillot_chardev serial0_chardev(&serial0, "serial0");	

extern genos::autom_schedee blink_schedee;

crow::hostaddr crowaddr = crow::address(".1.12.127.0.0.1:10009");


crow::self_driven_gstuff crowgate;
crow::service_node clinode;
char send_buffer[100];
#define CROW_PACKET_SIZE 90

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

void crow_service_handle(char* a, int b, crow::service_node& c)
{
	command(a, b, c);
}

int crow_write_callback(void * priv, const char *data, unsigned int size)
{
	(void) priv;
	return serial0.write(data, size);
}

void crow_services_init()
{
	crowgate.init(
	    send_buffer,
	    crow_write_callback,
	    NULL,
	    CROW_PACKET_SIZE);
	crowgate.bind(1);

	clinode.init(crow_service_handle);
	clinode.init_subscribe(crowaddr, CROWKER_SERVICE_BROCKER_NODE_NO, "zippo/ctr", 0, 0, 0, 0);
	clinode.bind(42);
	clinode.install_keepalive(2000);

	crow_schedee.start();
}