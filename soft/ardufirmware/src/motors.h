#ifndef ZIPPO_MOTORS_H
#define ZIPPO_MOTORS_H

#include <ralgo/robo/motor.h>
#include <zillot/arduino/libs/Adafruit_MotorShield/Adafruit_MotorShield.h>

extern Adafruit_MotorShield mshield;
extern volatile bool POWER_ENABLED;

extern volatile float lpower;
extern volatile float rpower;

struct motor_driver : public robo::motor
{
    Adafruit_DCMotor *M;

    uint8_t setted_mode = RELEASE;

    bool reverse = false;

    void power(float pwr) override;
    void stop() override;
};

extern motor_driver motors[4];
extern motor_driver &motor_fl;
extern motor_driver &motor_fr;
extern motor_driver &motor_bl;
extern motor_driver &motor_br;

void motors_stop();
void motors_run(float pwr);
void motors_run(float lpwr, float rpwr);
int updater(void *arg);

void motors_task_init();

#endif