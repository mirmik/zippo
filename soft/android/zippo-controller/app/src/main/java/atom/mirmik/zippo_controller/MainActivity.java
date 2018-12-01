package atom.mirmik.zippo_controller;

import android.view.WindowManager;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.hardware.SensorManager;
import android.hardware.Sensor;
import android.content.Context;
import android.hardware.SensorEventListener;
import android.hardware.SensorEvent;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class MainActivity extends AppCompatActivity {

    float[] acc = new float[3];
    float[] gyr = new float[3];
    float[] mag = new float[3];

    //final Lock lock = new ReentrantLock();
    //final Condition needUpdate  = lock.newCondition();

    long accTime = System.nanoTime();
    long gyrTime = System.nanoTime();
    long magTime = System.nanoTime();

    public class SensorListener implements SensorEventListener {
        @Override
        public void onSensorChanged(SensorEvent event) {
            switch (event.sensor.getType()) {
                case Sensor.TYPE_ACCELEROMETER:
                    acc[0] = event.values[0];
                    acc[1] = event.values[1];
                    acc[2] = event.values[2];
                    //System.out.println(String.format("acc (%f, %f, %f), d: %f", event.values[0], event.values[1], event.values[2], (float)(System.nanoTime() - accTime)/1000000));
                    accTime = System.nanoTime();
                    break;
                case Sensor.TYPE_GYROSCOPE:
                    gyr[0] = event.values[0];
                    gyr[1] = event.values[1];
                    gyr[2] = event.values[2];
                    //System.out.println(String.format("gyr (%f, %f, %f), d: %f", event.values[0], event.values[1], event.values[2], (float)(System.nanoTime() - gyrTime)/1000000));
                    gyrTime = System.nanoTime();
                    //needUpdate.

                    /*lock.lock();
                    try {
                        needUpdate.signal();
                    } finally {
                        lock.unlock();
                    }*/

                    break;
                case Sensor.TYPE_MAGNETIC_FIELD:
                    mag[0] = event.values[0];
                    mag[1] = event.values[1];
                    mag[2] = event.values[2];
                    //System.out.println(String.format("mag (%f, %f, %f), d: %f", event.values[0], event.values[1], event.values[2], (float)(System.nanoTime() - magTime)/1000000));
                    magTime = System.nanoTime();
                    break;
                default: publisher.publish("log", "Very Strange Situation".getBytes());
            }
        }

        @Override
        public void onAccuracyChanged(Sensor s, int i) {

        }
    }

    SensorListener listener;
    Publisher publisher;
    Thread ithr, hthr;

    private SensorManager mSensorManager;
    private Sensor sAcc, sGyr, sMag;

    public class PublishThread extends Thread {
        int i = 0;
        public void run(){
            ByteBuffer bbuf = ByteBuffer.allocate(36);
            bbuf.order(ByteOrder.LITTLE_ENDIAN);
            try {
                Thread.sleep(2000);
            }catch (Exception e) {
                System.out.println(e);
            }
            while(true) {
                bbuf.putFloat(0, acc[0]);
                bbuf.putFloat(4, acc[1]);
                bbuf.putFloat(8, acc[2]);
                bbuf.putFloat(12, gyr[0]);
                bbuf.putFloat(16, gyr[1]);
                bbuf.putFloat(20, gyr[2]);
                bbuf.putFloat(24, mag[0]);
                bbuf.putFloat(28, mag[1]);
                bbuf.putFloat(32, mag[2]);

                publisher.publish("ahrs", bbuf.array());

                try {
                    Thread.sleep(20);
                }catch (Exception e) {
                    System.out.println(e);
                }


                    //publisher.publish("hello", String.format("HelloWorld %d", i++).getBytes());
                    //publisher.publish("acc", String.format("acc (%f, %f, %f) ", acc[0], acc[1], acc[2]).getBytes());
                    //publisher.publish("gyr", String.format("gyr (%f, %f, %f) ", gyr[0], gyr[1], gyr[2]).getBytes());
                    //publisher.publish("mag", String.format("mag (%f, %f, %f) ", mag[0], mag[1], mag[2]).getBytes());
                    //try {
                    //    Thread.sleep(10);
                    //}catch (Exception e) {
                    //    System.out.println(e);
                    //}
            }
        }
    }

    public class ImuThread extends Thread {
        int i = 0;
        public void run(){
            listener = new SensorListener();
            mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD) != null){
                publisher.publish("log", "TYPE_MAGNETIC_FIELD ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_MAGNETIC_FIELD ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null){
                publisher.publish("log", "TYPE_ACCELEROMETER ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_ACCELEROMETER ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER_UNCALIBRATED) != null){
                publisher.publish("log", "TYPE_ACCELEROMETER_UNCALIBRATED ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_ACCELEROMETER_UNCALIBRATED ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY) != null){
                publisher.publish("log", "TYPE_GRAVITY ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_GRAVITY ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) != null){
                publisher.publish("log", "TYPE_GYROSCOPE ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_GYROSCOPE ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED) != null){
                publisher.publish("log", "TYPE_GYROSCOPE_UNCALIBRATED ... OK".getBytes());
            } else {
                publisher.publish("log", "TYPE_GYROSCOPE_UNCALIBRATED ... Don`t exist. ".getBytes());
            }

            sAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            sGyr = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
            sMag = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);

            mSensorManager.registerListener(listener, sAcc, SensorManager.SENSOR_DELAY_GAME);
            mSensorManager.registerListener(listener, sGyr, SensorManager.SENSOR_DELAY_GAME);
            mSensorManager.registerListener(listener, sMag, SensorManager.SENSOR_DELAY_GAME);
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        publisher = new Publisher();
        publisher.setHostAddress(".12.192.168.4.1:10009");

        hthr = new PublishThread();
        ithr = new ImuThread();
        ithr.start();
        hthr.start();

        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    }

    @Override
    public void onBackPressed() {
        finish();
        super.onBackPressed();
    }

    @Override
    public void onDestroy()
    {
        android.os.Process.killProcess(android.os.Process.myPid());
        super.onDestroy();
    }
}
