#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/time/systime.h>

#include <arch/i2c_automate.h>
#include <gxx/print.h>

#include <genos/schedule.h>
#include <genos/sched/tasklet.h>
#include <genos/sched/timer.h>
#include <genos/sched/schedee.h>

#include <genos/sched/process.h>
#include <gxx/debug/delay.h>

#include <genos/proclib.h>
#include <genos/addons/Adafruit_MotorShield/Adafruit_MotorShield.h>

#include <genos/robo/motor.h>

#include <crow/tower.h>
#include <crow/pubsub.h>
#include <genos/drivers/g1/uartgate.h>

#define WITHOUT_COMMAND_TIMEOUT 300

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);

arch::i2c_automate i2c;
Adafruit_MotorShield mshield;

genos::uartgate uartgate(&board::usart0, 128);

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


void error_handler() {
	dprln("error_handler");
}

char buf[64];

char stack[512];
char stack2[512];

void operation_finish_handler() {
	gxx::print_dump((const char*)buf, 2, 8);
}

void mainproc(void* arg);
void initproc(void* arg);


void traveling_handler(crow::packet* pack) {
	//dprln("travel");
}

void pubsub_handler(crow::packet* pack) {
	genos::create_process(mainproc, pack, stack).detach();
}

int main() {
	board_init();

	/*while(1) {
		board::led.tgl();
		debug_delay(40000);
	}	*/

	i2c.init_master();

	crow::traveling_handler = traveling_handler;

	crow::set_publish_host(crow::host("#F4.12.192.168.1.135:10009"));
	crow::set_publish_qos(crow::QoS(0));
	crow::link_gate(&uartgate, 0xF4);
	board::usart0.enable(false);
	board::usart0.setup(115200);
	uartgate.init();
	board::usart0.enable(true);

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	
	genos::hal::irqs::enable();
	genos::create_process(initproc, nullptr, stack).detach();

	
	crow::subscribe("turtle_power", crow::QoS(2));
	crow::pubsub_handler = pubsub_handler;

	//crow::send("\xF4", 1, "HelloWorld\n", 11);
	crow::publish("journal", "start schedule");

	//dprln("HERE");
	genos::schedule();
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
	//dprln("HERE");
	crow::publish("journal", gxx::format("here {}", i++).c_str());	
	crow::packet* pack = (crow::packet*) arg;
	
	/*gxx::buffer dsect = crow::pubsub_message_datasect(pack);

	using tt = struct{ float a; float b; };
	tt* s = (tt*) dsect.data(); 

	if (dsect.size() != 8) {
		crow::publish("journal","turtle_power wrong size");	
		crow::release(pack);
		return;
	}

	genos::set_wait_handler(i2c.operation_finish_handler);
	//motors_run(s->a, s->b);	
	motors_run(s->a, s->b);	*/
	
	crow::release(pack);
}

void initproc(void* arg) {
	genos::set_wait_handler(i2c.operation_finish_handler);
	mshield.begin(&i2c); 
} 

uint16_t crow::millis() {
	return systime::millis();
}

void genos::schedule() {
	while(1) {
		crow::onestep();
		genos::tasklet_manager.exec();
		genos::timer_manager.exec();
		genos::schedee_manager.exec();
	}
}