#include <Arduino.h>
#include <genos/autom_schedee.h>
#include <genos/schedee_api.h>

#include <blink_task.h>

void blink_task(void* priv, int* state) 
{
	(void) priv;
	(void) state;
	digitalWrite(13,!digitalRead(13));
	genos::current_schedee_msleep(100);
}

genos::autom_schedee blink_schedee(blink_task, nullptr);

void blink_task_init() 
{
	pinMode(13, 1);
	blink_schedee.start();
}