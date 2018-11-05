#include <hal/board.h>
#include <hal/irq.h>

#include <arch/i2c_automate.h>
#include <gxx/print.h>

#include <gxx/debug/delay.h>
#include <gxx/util/hexer.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <systime/systime.h>
#include <drivers/serial/avr_usart.h>
#include <drivers/crow/uartgate.h>
#include <sched/sched.h>

#include <addons/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <robo/motor.h>

#define WITHOUT_COMMAND_TIMEOUT 300

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

arch::i2c_automate i2c;
Adafruit_MotorShield mshield;

avr_usart usart0;
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

char stack[256];
char stack2[256];

void mainproc(void* arg);
void initproc(void* arg);

void pubsub_handler(crowket* pack) {
	//genos::create_process(mainproc, pack, stack).detach();
}

uint8_t raddr_[8];
int main() {
	const char * raddr = "#F4.12.192.168.1.135:10009"; 
	int raddr_len = hexer(raddr_, 8, raddr, strlen(raddr));

	board_init();
	schedee_manager_init();

	i2c.init_master();

	crow_set_publish_host(raddr_, raddr_len);
	//crow_link_gate(&uartgate.gw, 0xF4);
	//board::usart0.enable(false);
	//board::usart0.setup(115200);
	crow_uartgate_init(&uartgate, &usart0);
	//board::usart0.enable(true);

	/*motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);
	
	irqs_enable();
	genos::create_process(initproc, nullptr, stack).detach();
		
	crow::subscribe("turtle_power", crow::QoS(0));
	crow::pubsub_handler = pubsub_handler;

	crow::publish("zippo", "start schedule");
	genos::schedule();*/
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

int i = 0;
void mainproc(void* arg) {
	/*crow::publish("zippo", gxx::format("here {}", i++).c_str());	
	board::led.tgl();
	crow::packet* pack = (crow::packet*) arg;
	
	gxx::buffer dsect = crow::pubsub_message_datasect(pack);

	using tt = struct{ float a; float b; };
	tt* s = (tt*) dsect.data(); 

	

	if (dsect.size() != 8) {
		crow::publish("zippo","turtle_power wrong size");	
		crow::release(pack);
		return;
	}

	genos::set_wait_handler(i2c.operation_finish_handler);
	//motors_run(s->a, s->b);	
	motors_run(s->a, s->b);	
	
	crow::release(pack);*/
}

void initproc(void* arg) {
	/*genos::set_wait_handler(i2c.operation_finish_handler);
	mshield.begin(&i2c);*/ 
} 

uint16_t crow_millis() {
	return millis();
}

void __schedule__() {
	while(1) {
		crow_onestep();
		//tasklet_manager.exec();
		//timer_manager.exec();
		schedee_manager();
	}
}