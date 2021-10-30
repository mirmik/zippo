#ifndef ZIPPO_MOTORS_H
#define ZIPPO_MOTORS_H

#include <zillot/arduino/libs/Adafruit_MotorShield/Adafruit_MotorShield.h>
#include <ralgo/robo/motor.h>

extern Adafruit_MotorShield mshield;
extern bool POWER_ENABLED;

extern float lpower;
extern float rpower;

struct motor_driver : public robo::motor
{
	Adafruit_DCMotor* M;

	uint8_t setted_mode = RELEASE;

	bool reverse = false;

	void power(float pwr) override;
	void stop() override;
};

extern motor_driver motors[4];
extern motor_driver & motor_fl;
extern motor_driver & motor_fr;
extern motor_driver & motor_bl;
extern motor_driver & motor_br;

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);
void* updater(void* arg);

void motors_task_init();

#endif