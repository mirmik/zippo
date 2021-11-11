#include <command.h>
#include <motors.h>
#include <igris/shell/rshell_executor.h>
#include <igris/util/numconvert.h>
#include <crow/nodes/nospublisher.h>
#include <nos/print.h>
#include <genos/ktimer.h>

ktimer_head stop_timer;

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

	float a = atof32(argv[1], nullptr);
	float b = atof32(argv[2], nullptr);

	lpower = a;
	rpower = b;
	if (lpower != 0 || rpower != 0)
	{
		stop_timer.start = millis();
		ktimer_plan(&stop_timer);
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

int command(char * str, int len, char * ans, int ansmax)
{
	if (str[len - 1] == '\n') str[len - 1] = 0;
	int ret = 0;
	rshell_execute(str, commands, &ret, 0, ans, ansmax);
	return ret;
}

void stop_timer_handle(void *, struct ktimer_head *)
{
	lpower = 0;
	rpower = 0;
}

void commands_init()
{
	ktimer_init(&stop_timer, stop_timer_handle, nullptr, 0, 2000);
}