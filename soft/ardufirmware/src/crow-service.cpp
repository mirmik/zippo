#include <crow-service.h>
#include <crow/nodes/nospublisher.h>
#include <crow/crow.h>
#include <crow/constexpr_hexer.h>
#include <crow/nodes/service_node.h>
#include <crow/gates/self_driven_gstuff.h>
#include <zillot/serial/uartring.h>
#include <zillot/serial/avr_usart_device.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>
#include <zillot/ioflags.h>
#include <command.h>
#include <crow/packet.h>

extern genos::autom_schedee blink_schedee;
extern struct avr_usart_device_s usart0;
uint8_t crowaddr_buffer[16];
crow::hostaddr_view crowaddr;

/*template< size_t N >
constexpr std::array<char, N> constexpr_char_array( char const (&s)[N] )
{
	std::array<char, N> ret = {};
	for (size_t i = 0; i < N; ++i)
		ret[i] = s[i];
	return ret;
}
constexpr auto crowaddr_pair = crow::constexpr_hexer(constexpr_char_array(".1.12.127.0.0.1:10009"));
crow::hostaddr_view crowaddr(&*crowaddr_pair.first.begin(), crowaddr_pair.second);
*/

ZILLOT_DEF_UARTRING(serial0, &usart0.dev, 100, 16);

crow::self_driven_gstuff crowgate;
crow::service_node clinode;
char send_buffer[100];

#define CROW_PACKET_SIZE 90
//#define CROW_PACKET_TOTAL 3
//__attribute__((aligned(16)))
//uint8_t crow_pool_buffer[CROW_PACKET_SIZE * CROW_PACKET_TOTAL];

genos::autom_schedee crow_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	while (cdev_avail(&serial0.dev))
	{
		char c;
		cdev_read(&serial0.dev, &c, 1, 0);
		crowgate.newdata(c);
	}
	cdev_read(&serial0.dev, NULL, 0, IO_VIRTUAL_DISPLACE);
}, nullptr);

genos::autom_schedee crow_resubscribe_schedee([](void * priv, int * state)
{
	(void) priv;
	(void) state;
	clinode.subscribe(crowaddr, CROWKER_SERVICE_BROCKER_NODE_NO, "zippo/ctr", 0, 0, 0, 0);
	current_schedee_msleep(1000);
}, nullptr);

int crow_service_handle(char * a, int b, char * c, int d)
{
	return command(a, b, c, d);
}

int crow_write_callback(void * priv, const char *data, unsigned int size)
{
	(void) priv;
	return cdev_write(&serial0.dev, data, size, IO_NOBLOCK);
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

	clinode.init(crow_service_handle, 8);
	clinode.bind(42);

	uartring_install(&serial0, NULL);
	schedee_start(&crow_schedee);
	schedee_start(&crow_resubscribe_schedee);
}