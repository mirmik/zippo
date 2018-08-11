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
#include <genos/drivers/g1/uartgate.h>

#define WITHOUT_COMMAND_TIMEOUT 300

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
void mainproc2(void* arg);


int main() {
	board_init();
	i2c.init_master();

	genos::create_process(mainproc, nullptr, stack).detach();

	crow::link_gate(&uartgate, 10);
	uartgate.init();
	genos::hal::irqs::enable();

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	crow::send("\x0A", 1, "HelloWorld", 10);


	genos::schedule();
}

volatile int count = 3;
volatile int count2 = 5;

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

void mainproc(void* arg) {
	genos::set_wait_handler(i2c.operation_finish_handler);
	mshield.begin(&i2c); 


	motors_stop();
}


/*void mainproc2(void* arg) {
	while(1) {
		dprln("Mirmik was here2", count2, SP);
		//genos::displace();
		genos::sleep(1500);
		//genos::displace();
	}
}*/

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