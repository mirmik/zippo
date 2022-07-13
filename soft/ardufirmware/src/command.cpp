#include <command.h>
#include <motors.h>
#include <igris/shell/rshell_executor.h>
#include <igris/util/numconvert.h>
#include <crow/nodes/nospublisher.h>
#include <nos/print.h>
#include <genos/ktimer.h>
#include <crow/nodes/service_node.h>
#include <igris/util/numconvert.h>

genos::ktimer stop_timer;

int hello(int argc, char ** argv, char * ans, int ansmax)
{
	(void) argv;
	(void) argc;
	snprintf(ans, ansmax, "helloworld");
	return 10;
}

int power_enable(int argc, char ** argv, char * ans, int ansmax)
{
	(void) ans; (void) ansmax;
	if (argc < 2)
	{
		return 0;
	}

	if (strcmp(argv[1], "on") == 0)
	{
		POWER_ENABLED = 1;
	}

	else if (strcmp(argv[1], "off") == 0)
	{
		POWER_ENABLED = 0;
	}

	return 0;
}

int power_setup(int argc, char ** argv, char * ans, int ansmax)
{
	(void) ans; (void) ansmax;
	if (argc < 3)
	{
		return 0;
	}

	float a = igris_atof32(argv[1], nullptr);
	float b = igris_atof32(argv[2], nullptr);

	lpower = a;
	rpower = b;
	if (lpower != 0 || rpower != 0)
	{
		stop_timer.start = igris::millis();
		stop_timer.plan();
	}

	return 0;
}

rshell_command commands[] =
{
	{"hello", hello, NULL},
	{"enable", power_enable, NULL},
	{"power", power_setup, NULL},
	{NULL, NULL, NULL}
};

void command(igris::buffer buf)
{
	char * str = buf.data();
	size_t len = buf.size();
	char ansbuf[64];
	if (str[len - 1] == '\n') str[len - 1] = 0;
	int ret = 0;
	rshell_execute(str, commands, &ret, 0, ansbuf, 64);
}

void stop_timer_handle(void *, genos::ktimer*)
{
	lpower = 0;
	rpower = 0;
}

void commands_init()
{
	stop_timer.init(stop_timer_handle, nullptr, 0, 2000);
}