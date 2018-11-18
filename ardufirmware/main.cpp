#include <hal/board.h>
#include <hal/irq.h>

//#include <arch/i2c_automate.h>
#include <gxx/print.h>

#include <gxx/debug/delay.h>
#include <gxx/util/hexer.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <systime/systime.h>
#include <drivers/i2c/avr_i2c.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>
#include <sched/sched.h>
#include <sched/timer.h>

#include <addons/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <robo/motor.h>

#define WITHOUT_COMMAND_TIMEOUT 300

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

float lpower = 0;
float rpower = 0;

avr_i2c_device i2c;
Adafruit_MotorShield mshield;

avr_usart usart0(USART0, ATMEGA_IRQ_U0RX);
struct crow_uartgate uartgate;

struct motor_driver : public genos::robo::motor {
	Adafruit_DCMotor* M;

	uint8_t setted_mode = RELEASE;

	bool reverse = false;

	void power(float pwr) override {
		if (reverse) pwr = -pwr;

		if (pwr == 0) {
			M->run(RELEASE);
			M->setSpeed(0);
			setted_mode = RELEASE;
			return;
		}

		if (pwr > 0) {
			if (setted_mode == BACKWARD) { M->run(RELEASE); }
			M->setSpeed(pwr * 255);
			if (setted_mode != FORWARD) { M->run(FORWARD); }
			setted_mode = FORWARD;
			return;
		}

		if (pwr < 0) {
			if (setted_mode == FORWARD) { M->run(RELEASE); }
			M->setSpeed((-pwr) * 255);
			if (setted_mode != BACKWARD) { M->run(BACKWARD); }
			setted_mode = BACKWARD;
		}
	}

	void stop() override { 
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
void* spammer(void* arg);
void* updater(void* arg);

int i = 0;
void pubsub_handler(crowket* pack) 
{		
	gxx::buffer thmbuf = crow::pubsub::get_theme(pack);

	if (thmbuf == "zippo_control") 
	{
		board::sysled.toggle();

		gxx::buffer datbuf = crow::pubsub::get_data(pack);

		float l;
		float r;

		memcpy(&l, datbuf.data(), 4);
		memcpy(&r, datbuf.data() + 4, 4);

		lpower = l;
		rpower = r;
		//motors_run(l, r);
	}

	crow::release(pack);
}

/*void user_incoming_handler(crowket* pack) {
	board::sysled.toggle();
	crow::release(pack);
}*/

uint8_t raddr_[8];
int main() {
	//const char * raddr = "#F4.12.192.168.1.135:10009"; 
	const char * raddr = "#F4.12.192.168.1.135:10009"; 
	int raddr_len = hexer(raddr_, 8, raddr, strlen(raddr));

	board_init();
	schedee_manager_init();
	
	board::sysled.settings(GPIO_MODE_OUTPUT);
	board::sysled.set(1);

	usart0.setup(115200);
	usart0.enable();

	i2c.init_master();
	i2c.enable();

	crow_set_publish_host(raddr_, raddr_len);
	crow_uartgate_init(&uartgate, &usart0);
	crow_user_incoming_handler = NULL;
	crow_pubsub_handler = pubsub_handler;
	
	irqs_enable();
	delay(100);
	
	mshield.begin(&i2c);

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	crow::subscribe("zippo_control");

	//motors_run(0.2, 0.2);

	schedee_run(create_cooperative_schedee(updater, nullptr, 256));
		
	//crow::publish("mirmik", "HelloWorld");
//	crow::subscribe("turtle_power", crow::QoS(0));
//	crow::pubsub_handler = pubsub_handler;
//	crow::publish("zippo", "start schedule");
	__schedule__();

	//crow_spin();

	while(1);
}

void motors_stop() {
	for (auto m : motors) m.stop();
}

void motors_run(float pwr) {
	for (auto m : motors) m.power(pwr);	
}

void motors_run(float lpwr, float rpwr) {
	motor_br.power(rpwr);
	motor_bl.power(lpwr);
	motor_fl.power(lpwr);
	motor_fr.power(rpwr);
}

void* updater(void* arg) 
{
	while(1) {
		motors_run(lpower, rpower);
		msleep(100);
	}
}

void* spammer(void* arg) 
{
	while(1) {
		crow_publish("mirmik", "HelloWorld", 0, 200);
		//dprln("HelloWorld");
		msleep(500);
	}
} 

uint16_t crow_millis() {
	return millis();
}

void __schedule__() {
	while(1) {
		crow_onestep();
		timer_manager();
		schedee_manager();
	}
}