#include <genos/hal/board.h>
#include <genos/hal/irqs.h>
#include <genos/time/systime.h>

#include <arch/i2c_automate.h>
#include <gxx/print.h>

arch::i2c_automate i2c;

void error_handler() {
	dprln("error_handler");
}

char buf[64];

void operation_finish_handler() {
	gxx::print_dump((const char*)buf, 2, 8);
}

int main() {
	board_init();

	dprln("board init!");
	//debug_blink();

	const char* str = "HelloWorld";
	
	i2c.error_handler = error_handler;
	i2c.operation_finish_handler = operation_finish_handler;
	i2c.init_master();
	i2c.start_write(0x40, str);



	genos::hal::irqs::enable();

	while(1) {}
}