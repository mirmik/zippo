#include <igris.h>
#include <ralgo.h>
#include <genos.h>
#include <crow.h>

#include <ralgo/robo/quadgen4_arduino.h>
#include <ralgo/heimer2/stepctr.h>
#include <genos/vterm.h>
#include <genos/ktimer.h>
#include <igris/shell/mshell.h>
#include <igris/util/numconvert.h>

#include <crow/tower.h>
#include <crow/gates/self_driven_gstuff.h>

struct stepctr_controller stepctr;
struct quadgen4_arduino quadgen;
struct vterm_automate vterm;
struct ktimer_head calibrate_off_timer;

char vbuffer[48];
char vbufferh[48*5];

int CALIBRATE = 0;
int SPEED = 900;

int64_t target_position = 0;

void vtwrite(void *, const char * data, unsigned int size) 
{
  Serial.write(data, size);
}

int hello(int, char **) 
{
  Serial.println("Hello");
}

void calibrate_off(void *, struct ktimer_head * tim) 
{
  CALIBRATE = 0;
  int64_t pos = (int64_t)-1070 * (int64_t)2000;
  stepctr_controller_set_position(&stepctr, pos);
  target_position = 0;
  Serial.println("calibrate off");    
    Serial.println((int32_t)pos);
}

int calibrate(int, char **) 
{
  Serial.println("calibrate on");
  CALIBRATE = 1;
  ktimer_init(&calibrate_off_timer, calibrate_off, nullptr, millis(), 6000);
  ktimer_plan(&calibrate_off_timer);
}

int setpos(int, char ** argv) 
{
  stepctr_controller_set_position(&stepctr, atoi32(argv[1], 10, nullptr));
    Serial.println((int32_t)stepctr.virtual_pos);
}

int speed(int argc, char ** argv) 
{
  SPEED = atoi32(argv[1], 10, nullptr);
}

int help(int,char **);

int mov(int argc, char ** argv) 
{
  target_position = atoi32(argv[1], 10, nullptr);
}

struct mshell_command commands[] = 
{
  {"help", help, NULL},  
  {"hello", hello, NULL},  
  {"calibrate", calibrate, NULL},  
  {"mov", mov, NULL},  
  {"set", setpos, NULL},  
  {"speed", speed, NULL},  
  {NULL, NULL, NULL},  
};

int help(int, char **) 
{
  mshell_help(commands, vtwrite, nullptr);
}

void vtexecute(void *, const char * data, unsigned int size) 
{
  int retcode;
  int sts = mshell_execute(data, commands, &retcode);

  if (sts) 
  {
    Serial.println("Command not found");  
  }
}

void setup() {
  Serial.begin(115200);
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);

  quadgen4_arduino_init(&quadgen, 8, 10, 9, 11);
  stepctr_controller_init(&stepctr, quadgen4_arduino_set, &quadgen, 2000, 0.7);
  
  vterm_automate_init(&vterm, vbuffer, 48, vbufferh, 5);
  vterm_set_write_callback(&vterm, vtwrite, nullptr);
  vterm_set_execute_callback(&vterm, vtexecute, nullptr);
  vterm_automate_init_step(&vterm);
}

void loop() 
{
  if (CALIBRATE) 
  {
    stepctr_controller_shift(&stepctr, -SPEED);  
  }
  else 
  {
    int64_t diff = target_position - stepctr.virtual_pos / 2000;
    //Serial.println((int32_t)stepctr.virtual_pos);
    if (diff < 0) 
    {
        stepctr_controller_shift(&stepctr, -SPEED);    
    }  

    else if (diff > 0) 
    {
        stepctr_controller_shift(&stepctr, SPEED);    
    } 
  }

  while(Serial.available()) 
  {
    char  c = Serial.read();  
    vterm_automate_newdata(&vterm, c);
  }

  ktimer_manager_step(millis());
  delay(1);
}
