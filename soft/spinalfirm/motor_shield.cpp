#include <ralgo/robo/drivers/adafruit_motor.h>

Adafruit_MotorShield mshield;

robo::adafruit_motor_driver motors[4];
robo::adafruit_motor_driver & motor_fl = motors[0];
robo::adafruit_motor_driver & motor_fr = motors[1];
robo::adafruit_motor_driver & motor_bl = motors[2];
robo::adafruit_motor_driver & motor_br = motors[3];

void motors_init() 
{
#ifdef __ARDUINO__
	mshield.begin(&i2c);
#endif

	motor_bl.M = mshield.getMotor(1);
	motor_br.M = mshield.getMotor(2);
	motor_fr.M = mshield.getMotor(3);
	motor_fl.M = mshield.getMotor(4);

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