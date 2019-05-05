#define NOTRACE 1
#include <nos/trace.h>

#include <hal/board.h>
#include <hal/irq.h>

//#include <arch/i2c_automate.h>
#include <nos/print.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <crow/hexer.h>
#include <systime/systime.h>
#include <drivers/i2c/avr_i2c.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>
#include <sched/sched.h>
#include <sched/timer.h>

#include <addons/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <robo/motor.h>

#define WITHOUT_COMMAND_TIMEOUT 300
#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 5

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

uint8_t crow_pool_buffer[CROW_PACKET_SIZE * CROW_PACKET_TOTAL];

float lpower = 0;
float rpower = 0;

bool en = false;
avr_i2c_device i2c;
Adafruit_MotorShield mshield;

AVR_USART_DEVICE_DECLARE(usart0, USART0, ATMEGA_IRQ_U0RX);
struct crow_uartgate uartgate;

bool prevent_crowing = false;

struct motor_driver : public genos::robo::motor
{
	Adafruit_DCMotor* M;

	uint8_t setted_mode = RELEASE;

	bool reverse = false;

	void power(float pwr) override
	{
		if (reverse) pwr = -pwr;

		if (pwr == 0)
		{
			M->run(RELEASE);
			M->setSpeed(0);
			setted_mode = RELEASE;
			return;
		}

		if (pwr > 0)
		{
			if (setted_mode == BACKWARD) { M->run(RELEASE); }

			M->setSpeed(pwr * 255);

			if (setted_mode != FORWARD) { M->run(FORWARD); }

			setted_mode = FORWARD;
			return;
		}

		if (pwr < 0)
		{
			if (setted_mode == FORWARD) { M->run(RELEASE); }

			M->setSpeed((-pwr) * 255);

			if (setted_mode != BACKWARD) { M->run(BACKWARD); }

			setted_mode = BACKWARD;
		}
	}

	void stop() override
	{
		TRACE();
		power(0);
	}
};

motor_driver motors[4];
motor_driver & motor_fl = motors[0];
motor_driver & motor_fr = motors[1];
motor_driver & motor_bl = motors[2];
motor_driver & motor_br = motors[3];

char buf[64];

void* recvproc(void* arg);
void* initproc(void* arg);
void* spammer0(void* arg);
void* spammer1(void* arg);
void* spammer2(void* arg);
void* spammer3(void* arg);
void* updater(void* arg);

int32_t i = 0;
void pubsub_handler(crow::packet* pack)
{
	TRACE();
	igris::buffer thmbuf = crow::pubsub::get_theme(pack);

	if (thmbuf == "zippo_control")
	{
		igris::buffer datbuf = crow::pubsub::get_data(pack);

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
		//board::sysled.toggle();
		gpio_pin_toggle(&board_led);

		igris::buffer datbuf = crow::pubsub::get_data(pack);

		if (datbuf == "on")
		{
			gpio_pin_write(&board_led, 1);
			en = true;
		}

		else if (datbuf == "off")
		{
			gpio_pin_write(&board_led, 0);
			en = false;
		}
	}

	crow::release(pack);
}

/*void user_incoming_handler(crowket* pack) {
	board::sysled.toggle();
	crow::release(pack);
}*/

uint8_t raddr_[8];
int main()
{
	//const char * raddr = "#F4.12.192.168.1.135:10009";
	const char * raddr = "#F4.12.127.0.0.1:10009";
	int raddr_len = hexer(raddr_, 8, raddr, strlen(raddr));

	board_init();
	schedee_manager_init();

	crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);

	gpio_pin_settings(&board_led, GPIO_MODE_OUTPUT);
	gpio_pin_write(&board_led, 1);

	uart_device_setup(&usart0, 115200, 'n', 8, 1);

	i2c.init_master();
	i2c.enable();

	crow::set_publish_host(raddr_, raddr_len);
	uartgate.init(&usart0.dev);

	crow::user_incoming_handler = NULL;
	crow::pubsub_handler = pubsub_handler;

	irqs_enable();
	delay(100);

	mshield.begin(&i2c);

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	crow::subscribe("zippo_control");
	crow::subscribe("zippo_enable");

	//motors_run(0.2, 0.2);

	//schedee_run(create_cooperative_schedee(spammer0, nullptr, 128));
	//schedee_run(create_cooperative_schedee(spammer1, nullptr, 128));
	//schedee_run(create_cooperative_schedee(spammer2, nullptr, 256));
	//schedee_run(create_cooperative_schedee(spammer3, nullptr, 256));
	schedee_run(create_cooperative_schedee(updater, nullptr, 128));

	//crow::publish("mirmik", "HelloWorld");
//	crow::subscribe("turtle_power", crow::QoS(0));
//	crow::pubsub_handler = pubsub_handler;
//	crow::publish("zippo", "start schedule");
	__schedule__();

	//crow_spin();

	while (1);
}

void motors_stop()
{
	TRACE();

	for (auto m : motors) m.stop();
}

void motors_run(float pwr)
{
	TRACE();

	for (auto m : motors) m.power(pwr);
}

void motors_run(float lpwr, float rpwr)
{
	TRACE();
	motor_bl.power(lpwr);
	motor_fl.power(lpwr);
	motor_br.power(rpwr);
	motor_fr.power(rpwr);
}

void* updater(void* arg)
{
	TRACE();

	while (1)
	{
		//	prevent_crowing = true;
		if (en)
			motors_run(lpower, rpower);
		else
			motors_run(0, 0);

		//	prevent_crowing = false;
		//crow::publish("upd", "updated", 0, 200);
		msleep(100);
	}
}

void* spammer0(void* arg)
{
	TRACE();

	while (1)
	{
		char buf[20];
		i32toa(i++, buf, 10);

		crow::publish("mirmik0", buf, 0, 200);
		//dprln("HelloWorld");
		msleep(200);
	}
}

void* spammer1(void* arg)
{
	TRACE();

	while (1)
	{
		char buf[20];
		i32toa(i++, buf, 10);

		crow::publish("mirmik1", buf, 0, 200);
		//dprln("HelloWorld");
		msleep(200);
	}
}

void* spammer2(void* arg)
{
	TRACE();

	while (1)
	{
		char buf[20];
		i32toa(i++, buf, 10);

		crow::publish("mirmik2", buf, 0, 200);
		//dprln("HelloWorld");
		msleep(200);
	}
}

void* spammer3(void* arg)
{
	TRACE();

	while (1)
	{
		char buf[20];
		i32toa(i++, buf, 10);

		crow::publish("mirmik3", buf, 0, 200);
		//dprln("HelloWorld");
		msleep(200);
	}
}

void __schedule__()
{
	TRACE();

	while (1)
	{
		if (!prevent_crowing) crow::onestep();

		timer_manager_step();
		schedee_manager_step();
	}
}