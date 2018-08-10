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

arch::i2c_automate i2c;

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
	//debug_blink();

	//i2c.error_handler = error_handler;
	//i2c.operation_finish_handler = operation_finish_handler;
	//i2c.init_master();

	genos::create_process(mainproc, nullptr, stack).detach();
	genos::create_process(mainproc2, nullptr, stack2).detach();

	genos::hal::irqs::enable();

	dprln("start!");
	genos::schedule();
}

volatile int count = 3;
volatile int count2 = 5;

void mainproc(void* arg) {
	while(1) {
		dprln("Mirmik was here1", count, SP);
		genos::sleep(500);
		//genos::displace();
		//dprln("Mirmik was here3", count, SP);

		//debug_delay(20000);
	}
}

void mainproc2(void* arg) {
	while(1) {
		dprln("Mirmik was here2", count2, SP);
		//genos::displace();
		genos::sleep(1500);
		//genos::displace();
	}
}

void genos::schedule() {
	while(1) {
		genos::tasklet_manager.exec();
		genos::timer_manager.exec();
		genos::schedee_manager.exec();
	}
}