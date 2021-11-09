#include <motors.h>
#include <asm/irq.h>

#include <zillot/i2c/avr_i2c_device.h>
#include <zillot/serial/uartring.h>
#include <zillot/ioflags.h>
#include <ralgo/filter/aperiodic_filter.h>
#include <genos/schedee_api.h>
#include <genos/coop_schedee.h>


#include <avr/io.h>
#include <avr/interrupt.h>

extern struct uartring_s serial0;

DECLARE_AVR_I2C_WITH_IRQS(i2c)
Adafruit_MotorShield mshield;
bool POWER_ENABLED = false;

void* updater(void* arg);
char updater_schedee_heap[100];
genos::coop_schedee updater_schedee(updater, nullptr, (void*)updater_schedee_heap, 100);

float lpower = 0;
float rpower = 0;

motor_driver motors[4];
motor_driver & motor_fl = motors[0];
motor_driver & motor_fr = motors[1];
motor_driver & motor_bl = motors[2];
motor_driver & motor_br = motors[3];

//ralgo::aperiodic_filter<float> ver_filter(0.90, 0.1);
//ralgo::aperiodic_filter<float> hor_filter(0.90, 0.1);
ralgo::aperiodic_filter<float> left_filter(0.05, 0.01);
ralgo::aperiodic_filter<float> right_filter(0.05, 0.01);

void motor_driver::power(float pwr)
{
	if (reverse) pwr = -pwr;

	if (pwr == 0)
	{
		M->run(RELEASE);
		M->setSpeed(0);
		setted_mode = RELEASE;
		return;
	}

	if (pwr > 0)
	{
		if (setted_mode == BACKWARD) { M->run(RELEASE); }

		M->setSpeed(pwr * 255);

		if (setted_mode != FORWARD) { M->run(FORWARD); }

		setted_mode = FORWARD;
		return;
	}

	if (pwr < 0)
	{
		if (setted_mode == FORWARD) { M->run(RELEASE); }

		M->setSpeed((-pwr) * 255);

		if (setted_mode != BACKWARD) { M->run(BACKWARD); }

		setted_mode = BACKWARD;
	}
}

void motor_driver::stop()
{
	power(0);
}

void motors_stop()
{
	for (auto m : motors) m.stop();
}

void motors_run(float pwr)
{
	for (auto m : motors) m.power(pwr);
}

void motors_run(float lpwr, float rpwr)
{
	motor_bl.power(lpwr);
	motor_fl.power(lpwr);
	motor_br.power(rpwr);
	motor_fr.power(rpwr);
}

void* updater(void* arg)
{
	(void)arg;

	avr_i2c_device_init_master(&i2c, 100000);
	avr_i2c_device_enable();

	mshield.begin(&i2c.dev);

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

	systime_t last_time = millis();
	while (1)
	{
		auto curtime = millis();
		if (POWER_ENABLED)
		{
			auto delta = (curtime - last_time) * 0.001;

			motors_run(
				left_filter.serve(lpower, delta), 
				right_filter.serve(rpower, delta));
		}
		else {
			left_filter.reset(0);
			right_filter.reset(0);
			motors_run(0, 0);
		}

		last_time = curtime;
		current_schedee_msleep(10);
	}

	return NULL;
}

void motors_task_init() 
{
	schedee_start(&updater_schedee);
}
