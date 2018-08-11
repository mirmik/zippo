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

arch::i2c_automate i2c;
Adafruit_MotorShield mshield;

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
	//genos::create_process(mainproc2, nullptr, stack2).detach();

	genos::hal::irqs::enable();

	dprln("start!");
	genos::schedule();
}

volatile int count = 3;
volatile int count2 = 5;

void mainproc(void* arg) {
	dprln("Mirmik was here1", count, SP);

	genos::set_wait_handler(i2c.operation_finish_handler);

	Adafruit_DCMotor *myMotor = mshield.getMotor(1);

	mshield.begin(&i2c);  // create with the default frequency 1.6KHz
	//AFMS.begin(1000);  // OR with a different frequency, say 1KHz
	
	// Set the speed to start, from 0 (off) to 255 (max speed)
	myMotor->setSpeed(20);
	myMotor->run(FORWARD);

	genos::sleep(1000);
	myMotor->setSpeed(50);

	genos::sleep(1000);
	myMotor->setSpeed(100);

	genos::sleep(1000);
	myMotor->setSpeed(150);

	genos::sleep(1000);
	myMotor->setSpeed(200);

	genos::sleep(1000);
	myMotor->run(RELEASE);
	
	//mshield.reset();
	//mshield.setPWMFreq(1600);

	gxx::println("end of process");
}

/*void mainproc2(void* arg) {
	while(1) {
		dprln("Mirmik was here2", count2, SP);
		//genos::displace();
		genos::sleep(1500);
		//genos::displace();
	}
}*/

void genos::schedule() {
	while(1) {
		genos::tasklet_manager.exec();
		genos::timer_manager.exec();
		genos::schedee_manager.exec();
	}
}