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
#include <zillot/ioflags.h>
#include <command.h>
#include <crow/packet.h>

extern genos::autom_schedee blink_schedee;
extern zillot::avr::usart usart0;

crow::hostaddr_view crowaddr;

ZILLOT_UARTRING(serial0, usart0, 100, 16);

crow::self_driven_gstuff crowgate;
crow::service_node clinode;
char send_buffer[100];
uint8_t crowaddr_buffer[16];
#define CROW_PACKET_SIZE 60

genos::autom_schedee crow_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	while (serial0.avail())
	{
		char c;
		serial0.read(&c, 1);
		crowgate.newdata(c);
	}
	//serial0.read(NULL, 0); // здесь надо наколдовать ожидание.
}, nullptr);

genos::autom_schedee crow_resubscribe_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	//clinode.subscribe(crowaddr, CROWKER_SERVICE_BROCKER_NODE_NO, "zippo/ctr", 0, 0, 0, 0);
	current_schedee_msleep(1000);
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

const char * caddr = ".1.12.127.0.0.1:10009";
void crow_services_init()
{
	memset(crowaddr_buffer, 0, 16);
	int l = hexer_s(crowaddr_buffer, 16, caddr);
	crowaddr = crow::hostaddr_view(crowaddr_buffer, l);

	//crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);
	crowgate.init(
	    send_buffer,
	    crow_write_callback,
	    NULL,
	    CROW_PACKET_SIZE);
	crowgate.bind(1);

	clinode.init(crow_service_handle);
	clinode.bind(42);

	schedee_start(&crow_schedee);
	schedee_start(&crow_resubscribe_schedee);
}