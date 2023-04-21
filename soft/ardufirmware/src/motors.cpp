#include <Arduino.h>
#include <asm/irq.h>
#include <avr/interrupt.h>
#include <avr/io.h>
#include <genos/coop_schedee.h>
#include <genos/schedee_api.h>
#include <motors.h>
#include <nos/print.h>
#include <ralgo/filter/aperiodic_filter.h>
#include <zillot/avr/avr_i2c_device.h>
#include <zillot/common/uartring.h>
#include <zillot/ioflags.h>

extern struct uartring_s serial0;

DECLARE_AVR_I2C_WITH_IRQS(i2c)
Adafruit_MotorShield mshield;
volatile bool POWER_ENABLED = false;

int updater(void *arg);
char updater_schedee_heap[200];
genos::coop_schedee updater_schedee(updater,
                                    nullptr,
                                    (void *)updater_schedee_heap,
                                    sizeof(updater_schedee_heap));

volatile float lpower = 0;
volatile float rpower = 0;

motor_driver motors[4];
motor_driver &motor_fl = motors[0];
motor_driver &motor_fr = motors[1];
motor_driver &motor_bl = motors[2];
motor_driver &motor_br = motors[3];

// ralgo::aperiodic_filter<float> ver_filter(0.90, 0.1);
// ralgo::aperiodic_filter<float> hor_filter(0.90, 0.1);
// ralgo::aperiodic_filter<float> left_filter(0.1, 0.1);
// ralgo::aperiodic_filter<float> right_filter(0.1, 0.1);

void motor_driver::power(float pwr)
{
    if (reverse)
        pwr = -pwr;

    if (pwr == 0)
    {
        M->run(RELEASE);
        M->setSpeed(0);
        setted_mode = RELEASE;
        return;
    }

    if (pwr > 0)
    {
        if (setted_mode == BACKWARD)
        {
            M->run(RELEASE);
        }

        M->setSpeed(pwr * 255);

        if (setted_mode != FORWARD)
        {
            M->run(FORWARD);
        }

        setted_mode = FORWARD;
        return;
    }

    if (pwr < 0)
    {
        if (setted_mode == FORWARD)
        {
            M->run(RELEASE);
        }

        M->setSpeed((-pwr) * 255);

        if (setted_mode != BACKWARD)
        {
            M->run(BACKWARD);
        }

        setted_mode = BACKWARD;
    }
}

void motor_driver::stop()
{
    power(0);
}

void motors_stop()
{
    for (auto m : motors)
        m.stop();
}

void motors_run(float pwr)
{
    for (auto m : motors)
        m.power(pwr);
}

void motors_run(float lpwr, float rpwr)
{
    motor_bl.power(lpwr);
    motor_fl.power(lpwr);
    motor_br.power(rpwr);
    motor_fr.power(rpwr);
}

int updater(void *arg)
{
    (void)arg;

    avr_i2c_device_init_master(&i2c, 100000);
    avr_i2c_device_enable();

    mshield.begin(&i2c.dev);

    motor_bl.M = mshield.getMotor(1);
    motor_br.M = mshield.getMotor(2);
    motor_fr.M = mshield.getMotor(3);
    motor_fl.M = mshield.getMotor(4);

    auto last_time = igris::millis();
    while (1)
    {
        auto curtime = igris::millis();
        if (POWER_ENABLED)
        {
            motors_run(lpower, rpower
                       //	left_filter.serve((float)lpower),
                       //	right_filter.serve((float)rpower)
            );
        }
        else
        {
            // left_filter.reset(0);
            // right_filter.reset(0);
            motors_run(0, 0);
        }

        last_time = curtime;
        (void)last_time;

        digitalWrite(13, !digitalRead(13));
        genos::current_schedee_msleep(50);
    }

    return 0;
}

void motors_task_init()
{
    schedee_start(&updater_schedee);
}
