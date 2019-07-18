#include <hal/board.h>
#include <hal/irq.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <crow/hexer.h>
#include <systime/systime.h>
#include <drivers/i2c/avr_i2c.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>

#include <genos/sched.h>
#include <genos/schedee/coop.h>
#include <genos/schedee/autom.h>

#include <genos/ktimer.h>

#include <addons/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <robo/motor.h>

#include <drivers/pwmservo/avr_pwmservo.h>
#include <addons/arduino/pwm.h>
#include <addons/arduino/pin.h>
#include <drivers/timer/avr_timer.h>

#include <igris/util/numconvert.h>

#include <ralgo/lintrans.h>

#define WITHOUT_COMMAND_TIMEOUT 300
#define CROW_PACKET_SIZE 64
#define CROW_PACKET_TOTAL 8

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

uint8_t crow_pool_buffer[CROW_PACKET_SIZE * CROW_PACKET_TOTAL] __attribute__((aligned(16)));

float lpower = 0;
float rpower = 0;

bool en = false;
avr_i2c_device i2c;
Adafruit_MotorShield mshield;

struct crow_uartgate uartgate;

bool prevent_crowing = false;

genos::coopschedee updater_schedee;
char updater_schedee_heap[128];

//pwmservo<uint16_t> servo0(&TIMER1->ocr_a, 0, 90, 1, 0x03FF);
//pwmservo<uint16_t> servo1(&TIMER1->ocr_b, 0, 90, 1, 0x03FF);

genos::avr::pwmservo pwm_ver;
genos::avr::pwmservo pwm_hor;

genos::avr::pwmservo_writer<uint16_t> wr_ver;
genos::avr::pwmservo_writer<uint16_t> wr_hor;

ralgo::lintrans::aperiodic<float> ver_filter(0.90, 0.1);
ralgo::lintrans::aperiodic<float> hor_filter(0.90, 0.1);

ralgo::lintrans::aperiodic<float> left_filter(0.05, 0.01);
ralgo::lintrans::aperiodic<float> right_filter(0.05, 0.01);

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

genos::autom_schedee spammer_schedee{spammer0, nullptr};

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


	else if (thmbuf == "zippo_shor")
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
	}

	crow::release(pack);
}

/*void user_incoming_handler(crowket* pack) {
	board::sysled.toggle();
	crow::release(pack);
}*/

uint8_t raddr_[16];
int raddr_len;
int main()
{
	//const char * raddr = "#F4.12.192.168.1.135:10009";
	board_init();
	//while(1)
	//dprln("INITED");

	pwm_hor = arduino_pwm_timer(9);
	pwm_ver = arduino_pwm_timer(10);

	pwm_hor.standart_timer_mode();
	pwm_hor.pwm_mode_start();
	wr_hor = pwm_hor.get_writer(1000, 2000);

	pwm_ver.standart_timer_mode();
	pwm_ver.pwm_mode_start();
	wr_ver = pwm_ver.get_writer(1000, 2000);

	pinMode(9,1);
	pinMode(10,1);

	wr_hor.set(0.5);
	wr_ver.set(0.5);

	/*periph::timer1.set_mode(decltype(periph::timer1)::TimerMode::Clock);
	periph::timer1.set_divider(64);
	//servo0.set(0.5);
	//servo1.set(0.5);
	periph::timer1.set_output_a_mode(0b10);
	periph::timer1.set_output_b_mode(0b10);

	periph::timer1.set_compare_a(0x1FF);
	periph::timer1.set_compare_b(0x1FF);*/

	gpio_settings(GPIOB, (1<<0) | (1<<1), GPIO_MODE_OUTPUT);

	const char * raddr = "#F4.12.127.0.0.1:10009";
	raddr_len = hexer(raddr_, 16, raddr, strlen(raddr));

	usart0.setup(115200, 'n', 8, 1);

	scheduler_init();
	crow::engage_packet_pool(crow_pool_buffer, CROW_PACKET_SIZE * CROW_PACKET_TOTAL, CROW_PACKET_SIZE);

	gpio_pin_settings(&board_led, GPIO_MODE_OUTPUT);
	gpio_pin_write(&board_led, 1);

	uartgate.init(&usart0);

	crow::user_incoming_handler = NULL;
	crow::pubsub_protocol.incoming_handler = pubsub_handler;

	crow::pubsub_protocol.enable();	

	irqs_enable();
	delay(100);

	//crow::diagnostic_enable();

	crow::subscribe(raddr_, raddr_len, "zippo_enable", 1, 200, 0, 200);
	crow::subscribe(raddr_, raddr_len, "zippo_control", 1, 200, 0, 200);
	crow::subscribe(raddr_, raddr_len, "zippo_shor", 1, 200, 0, 200);
	crow::subscribe(raddr_, raddr_len, "zippo_sver", 1, 200, 0, 200);

	//motors_run(0.2, 0.2);

	//spammer_schedee.run();


	updater_schedee.init(updater, nullptr, updater_schedee_heap, 128);
	updater_schedee.run();

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
			motors_run(left_filter(lpower), right_filter(rpower));
		}
		else {
			left_filter.set_value(0);
			right_filter.set_value(0);
			motors_run(0, 0);
		}

		msleep(10);
	}
}

void* spammer0(void* arg, int* state)
{
	char buf[20];
	i32toa(i++, buf, 10);

	crow::publish(raddr_, raddr_len, "mirmik0", buf, 0, 200);
	msleep(1000);
}

void __schedule__()
{
	while (1)
	{
		dprln("HERE");
		if (!prevent_crowing)
			crow::onestep();

		ktimer_manager_step();
		schedee_manager_step();
	}
}