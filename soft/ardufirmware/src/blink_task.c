#include <Arduino.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>

#include <blink_task.h>

struct autom_schedee blink_schedee;

void blink_task(void* priv, int* state) 
{
	(void) priv;
	(void) state;
	digitalWrite(13,!digitalRead(13));
	current_schedee_msleep(1000);
}

void blink_task_init() 
{
	pinMode(13, 1);
	autom_schedee_init(&blink_schedee, blink_task, NULL);
	schedee_start(&blink_schedee.sch);
}