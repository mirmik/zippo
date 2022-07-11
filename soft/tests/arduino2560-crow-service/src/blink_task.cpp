#include <Arduino.h>
#include <zillot/common/uartring.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>

#include <blink_task.h>

extern zillot::uartring serial0;

void blink_task(void* priv, int* state) 
{
	(void) priv;
	(void) state;
	digitalWrite(13,!digitalRead(13));
	serial0.println(igris::millis());
	genos::current_schedee_msleep(500);
}

genos::autom_schedee blink_schedee(blink_task, nullptr);

void blink_task_init() 
{
	pinMode(13, 1);
	schedee_start(&blink_schedee);
}