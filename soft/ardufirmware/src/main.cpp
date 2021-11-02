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
#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 8

__attribute__((aligned(16)))
uint8_t crow_pool_buffer[CROW_PACKET_SIZE * CROW_PACKET_TOTAL];

DECLARE_AVR_USART_WITH_IRQS(usart0, USART0, USART);
DECLARE_AVR_I2C_WITH_IRQS(i2c);

/*#include <crow/tower.h>
#include <crow/pubsub/pubsub.h>
#include <crow/hexer.h>
#include <systime/systime.h>
#include <drivers/i2c/avr_i2c.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>

#include <asm/avr_gpio.h>

#include <genos/sched.h>
#include <genos/schedee/coop.h>
#include <genos/schedee/autom.h>

#include <genos/ktimer.h>

#include <drivers/pwmservo/avr_pwmservo.h>
//#include <addons/arduino/pwm.h>
//#include <addons/arduino/pin.h>
#include <drivers/timer/avr_timer.h>

#include <igris/util/numconvert.h>

#include <ralgo/lintrans.h>
#include <drivers/gpio/avr_gpio.h>

#include <genos/api.h>

#include <Arduino.h>

#define WITHOUT_COMMAND_TIMEOUT 300
#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 8*/
/*
void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

bool en = false;

struct crow_uartgate uartgate;

bool prevent_crowing = false;

//pwmservo<uint16_t> servo0(&TIMER1->ocr_a, 0, 90, 1, 0x03FF);
//pwmservo<uint16_t> servo1(&TIMER1->ocr_b, 0, 90, 1, 0x03FF);

//genos::avr::pwmservo pwm_ver;
//genos::avr::pwmservo pwm_hor;

//genos::avr::pwmservo_writer<uint16_t> wr_ver;
//genos::avr::pwmservo_writer<uint16_t> wr_hor;

extern avr_gpio_pin board_led;

*/

/*
char buf[64];

void* recvproc(void* arg);
void* initproc(void* arg);
void* spammer0(void* arg, int* state);
void* updater(void* arg);

genos::autom_schedee spammer_schedee{spammer0, nullptr};
*/
int32_t i = 0;
void pubsub_handler(crow::packet* pack)
{
/*	auto psptr = crow::pubsub_packet_ptr(pack);

	igris::buffer thmbuf = psptr.theme();
	//crow::send("\xF4", 1, "fsdfa", 5, 0, 0, 200);

	if (thmbuf == "zippo_control")
	{
		igris::buffer datbuf = psptr.message();

		float l;
		float r;

		memcpy(&l, datbuf.data(), 4);
		memcpy(&r, datbuf.data() + 4, 4);

		lpower = l;
		rpower = r;
		//motors_run(l, r);
	}

	else if (thmbuf == "zippo_enable")
	{
		igris::buffer datbuf = psptr.message();

		if (datbuf == "on")
		{
			digitalWrite(13, 1);
			POWER_ENABLED = true;
		}

		else if (datbuf == "off")
		{
			digitalWrite(13, 0);
			POWER_ENABLED = false;
		}
	}
*/

	/*else if (thmbuf == "zippo_shor")
	{
		igris::buffer datbuf = crow::pubsub::get_data(pack);

		float l;
		memcpy(&l, datbuf.data(), 4);
		wr_hor.set(hor_filter(l));
	}


	else if (thmbuf == "zippo_sver")
	{
		igris::buffer datbuf = crow::pubsub::get_data(pack);

		float l;
		memcpy(&l, datbuf.data(), 4);
		wr_ver.set(ver_filter(l));
	}*/

	crow::release(pack);
}

/*void user_incoming_handler(crowket* pack) {
	board::sysled.toggle();
	crow::release(pack);
}*/

uint8_t raddr_[16];
size_t raddr_len;

int main()
{
	arch_init();
	schedee_manager_init();
	crow_services_init();

	irqs_enable();
    avr_usart_setup(USART0, 115200, 'n', 8, 1);

	pinMode(13,1);
	pinMode(9,1);
	pinMode(10,1);

	blink_task_init();
	motors_task_init();

	while(1)
		__schedule__();

	const char * raddr = "#F4.12.127.0.0.1:10009";
	raddr_len = hexer(raddr_, 16, raddr, strlen(raddr));

	avr_usart_setup(USART0, 115200, 'n', 8, 1);

	schedee_manager_init();
	crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);

//	uartgate.init(&usart0, 42);

	crow::user_incoming_handler = NULL;
//	crow::pubsub_protocol.incoming_handler = pubsub_handler;

	irqs_enable();
	delay(100);

//	crow::subscribe({raddr_, raddr_len}, "zippo_enable", 1, 200, 0, 200);
//	crow::subscribe({raddr_, raddr_len}, "zippo_control", 1, 200, 0, 200);
//	crow::subscribe({raddr_, raddr_len}, "zippo_shor", 1, 200, 0, 200);
//	crow::subscribe({raddr_, raddr_len}, "zippo_sver", 1, 200, 0, 200);

	while (1)
		__schedule__();
}

void __schedule__()
{
	while (1)
	{
		auto curtime = millis();

		ktimer_manager_step(curtime);
		schedee_manager_step();
	}
}