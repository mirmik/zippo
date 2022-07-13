//#include <crow-service.h>
//#include <crow/nodes/nospublisher.h>
//#include <crow/crow.h>
//#include <crow/constexpr_hexer.h>
//#include <crow/nodes/subscriber_node.h>
//#include <crow/gates/self_driven_gstuff.h>
#include <zillot/common/uartring.h>
#include <zillot/avr/usart.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>
#include <genos/chardev.h>
#include <zillot/ioflags.h>
#include <igris/protocols/gstuff.h>
#include <command.h>
//#include <crow/packet.h>

extern zillot::avr::usart usart0;
ZILLOT_UARTRING(serial0, usart0, 90, 16);
genos::zillot_chardev serial0_chardev(&serial0, "serial0");	

uint8_t buffer[56];
gstuff_autorecv autorecv;

/*extern genos::autom_schedee blink_schedee;
crow::self_driven_gstuff crowgate;
crow::subscriber_node clinode;
char send_buffer[95];

crow::hostaddr crowaddr = crow::address(".1.12.127.0.0.1:10009");*/

void newline() 
{
	dprln("newline:", autorecv.cstr());
	command({autorecv.cstr(), autorecv.size()});
}

genos::autom_schedee crow_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	while (serial0.avail())
	{
		char c;
		serial0.read(&c, 1);		
		auto ret = autorecv.newchar(c);
		if (ret == GSTUFF_NEWPACKAGE)
			newline();
	}
	serial0_chardev.read(NULL, 0);
}, nullptr);
/*
void crow_service_handle(igris::buffer buf, crow::subscriber_node& node)
{
	command(buf);
}*/
/*
int crow_write_callback(void * priv, const char *data, unsigned int size)
{
	(void) priv;
	return serial0.write(data, size);
}
int crow_room_callback(void * priv)
{
	(void) priv;
	return serial0.room();
}*/

void crow_services_init()
{
	serial0.begin();

	/*crowgate.init(
	    send_buffer,
	    crow_write_callback,
	    crow_room_callback,
	    NULL,
	    64);
	crowgate.bind(1);

	clinode.set_handle(crow_service_handle);
	clinode.init_subscribe(crowaddr, CROWKER_SERVICE_BROCKER_NODE_NO, "zippo/ctr", 0, 0, 0, 0);
	clinode.bind(42);
	clinode.install_keepalive(2000);
*/
	autorecv.setbuf(buffer, 56);
	autorecv.reset();
	crow_schedee.start();
}