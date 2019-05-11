#define NOTRACE 1
#include <nos/trace.h>

#include <hal/board.h>
#include <hal/irq.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <crow/hexer.h>
#include <systime/systime.h>
#include <drivers/i2c/avr_i2c.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>

#include <sched/sched.h>
#include <sched/schedee/cooperative.h>
#include <sched/schedee/autom.h>

#include <genos/ktimer.h>

#include <addons/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <robo/motor.h>

#define WITHOUT_COMMAND_TIMEOUT 300
#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 4

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

struct cooperative_schedee updater_schedee;
char updater_schedee_heap[128];

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
void* spammer0(void* arg, int* state);
void* updater(void* arg);

int32_t i = 0;
void pubsub_handler(crow::packet* pack)
{
	igris::buffer thmbuf = crow::pubsub::get_theme(pack);
	//crow::send("\xF4", 1, "fsdfa", 5, 0, 0, 200);

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
		//crow::send("\xF4", 1, "fsdfa", 5, 0, 0, 200);
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

uint8_t raddr_[16];
int main()
{
	//const char * raddr = "#F4.12.192.168.1.135:10009";
	board_init();

	const char * raddr = "#F4.12.127.0.0.1:10009";
	int raddr_len = hexer(raddr_, 16, raddr, strlen(raddr));

	uart_device_setup(&usart0, 115200, 'n', 8, 1);

	scheduler_init();
	crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);

	gpio_pin_settings(&board_led, GPIO_MODE_OUTPUT);
	gpio_pin_write(&board_led, 1);


	crow::set_publish_host(raddr_, raddr_len);
	uartgate.init(&usart0.dev);

	crow::user_incoming_handler = NULL;
	crow::pubsub_handler = pubsub_handler;

	irqs_enable();
	delay(100);

	//crow::diagnostic_enable();

	crow::subscribe("zippo_enable");
	crow::subscribe("zippo_control");

	//motors_run(0.2, 0.2);

	//schedee_run(create_autom_schedee(spammer0, nullptr));


	cooperative_schedee_init(&updater_schedee, updater, nullptr, updater_schedee_heap, 128);
	schedee_run(&updater_schedee.sch);

	while (1)
		__schedule__();
}

void motors_stop()
{
	for (auto m : motors) m.stop();
}

void motors_run(float pwr)
{
	for (auto m : motors) m.power(pwr);
}

void motors_run(float lpwr, float rpwr)
{

	motor_bl.power(lpwr);
	motor_fl.power(lpwr);
	motor_br.power(rpwr);
	motor_fr.power(rpwr);
}

void* updater(void* arg)
{
	irqs_enable();

	//dprln("i2c init master");
	i2c.init_master();
	//msleep(2000);

	//dprln("i2c enable");
	i2c.enable();
	//msleep(2000);

	//dprln("mshield begin");
	mshield.begin(&i2c);
	//msleep(2000);

	//dprln("mshield motors registry begin");
	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	while (1)
	{
		if (en)
		{
			//crow::send("\xF4", 1, "Asdfa", 5, 0, 0, 200);
			motors_run(lpower, rpower);
		}
		else
			motors_run(0, 0);

		msleep(100);
	}
}

void* spammer0(void* arg, int* state)
{


	char buf[20];
	i32toa(i++, buf, 10);

	crow::publish("mirmik0", buf, 0, 200);
	msleep(200);
}

void __schedule__()
{
	while (1)
	{
		if (!prevent_crowing)
			crow::onestep();

		timer_manager_step();
		schedee_manager_step();
	}
}