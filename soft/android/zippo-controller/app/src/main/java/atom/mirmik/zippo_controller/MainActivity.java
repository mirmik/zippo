package atom.mirmik.zippo_controller;

import android.content.Intent;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.WindowManager;

import android.app.*;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.AsyncTask;
import android.hardware.SensorManager;
import android.hardware.Sensor;
import android.content.Context;
import android.hardware.SensorEventListener;
import android.hardware.SensorEvent;
import android.widget.TextView;
import android.widget.Toolbar;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class MainActivity extends AppCompatActivity {

    float[] acc = new float[3];
    float[] gyr = new float[3];
    float[] mag = new float[3];

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
                    accTime = System.nanoTime();
                    break;
                case Sensor.TYPE_GYROSCOPE:
                    gyr[0] = event.values[0];
                    gyr[1] = event.values[1];
                    gyr[2] = event.values[2];
                    gyrTime = System.nanoTime();

                    break;
                case Sensor.TYPE_MAGNETIC_FIELD:
                    mag[0] = event.values[0];
                    mag[1] = event.values[1];
                    mag[2] = event.values[2];
                    magTime = System.nanoTime();
                    break;
                default:
                        publisher.publish_noexcept("log", "Very Strange Situation".getBytes());

            }
        }

        @Override
        public void onAccuracyChanged(Sensor s, int i) {

        }
    }

    SensorListener listener;
    TcpPublisher publisher;
    Thread ithr, hthr;

    private SensorManager mSensorManager;
    private Sensor sAcc, sGyr, sMag;

    public class PublishThread extends Thread {
        int i = 0;
        public void run(){
            ByteBuffer bbuf = ByteBuffer.allocate(36);
            bbuf.order(ByteOrder.LITTLE_ENDIAN);

            try
            {
                Thread.sleep(2000);
            }
            catch (Exception e)
            {
                System.out.println(e);
            }

            while(true)
            {
                bbuf.putFloat(0, acc[0]);
                bbuf.putFloat(4, acc[1]);
                bbuf.putFloat(8, acc[2]);
                bbuf.putFloat(12, gyr[0]);
                bbuf.putFloat(16, gyr[1]);
                bbuf.putFloat(20, gyr[2]);
                bbuf.putFloat(24, mag[0]);
                bbuf.putFloat(28, mag[1]);
                bbuf.putFloat(32, mag[2]);

                if (sp.getBoolean("sensors_spam", true))
                    publisher.publish_noexcept("ahrs", bbuf.array());

                try {
                    Thread.sleep(20);
                }catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    boolean connectionState = false;

    public void connectDisconnectActionClick(View view)
    {
        final MainActivity ma = this;
        final AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("connection error").setTitle("NotConnect");
        final AlertDialog dialog = builder.create();

        if (connectionState == true)
        {
            AsyncTask.execute(new Runnable() {
                @Override
                public void run()
                {
                    publisher.disconnect();
                }
            });
            return;
        }

        else {
            AsyncTask.execute(new Runnable() {
                @Override
                public void run() {
                    String ip = sp.getString("ip", "127.0.0.1");
                    String port = sp.getString("port", "10010");

                    try {
                        publisher.connect(ip, Integer.valueOf(port));
                    } catch (IOException ex) {
                        System.out.println("connection error");

                        ma.runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                if (!dialog.isShowing()) {
                                    dialog.show();
                                }
                                dialog.setMessage("connection error");
                            }
                        });
                    }
                }
            });
        }
    }

    public void settingsActionClick(View view)
    {
        Intent i = new Intent(this, Settings.class);
        startActivity(i);
    }

    public void enableCommandSend(View view) {
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                publisher.publish_noexcept("zippo_enable", "on".getBytes());
            }
        });
    }

    public void disableCommandSend(View view) {
        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                publisher.publish_noexcept("zippo_enable", "off".getBytes());
            }
        });
    }

    public class ImuThread extends Thread {
        int i = 0;
        public void run(){
            listener = new SensorListener();
            mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD) != null){
                publisher.publish_noexcept("log", "TYPE_MAGNETIC_FIELD ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_MAGNETIC_FIELD ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null){
                publisher.publish_noexcept("log", "TYPE_ACCELEROMETER ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_ACCELEROMETER ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER_UNCALIBRATED) != null){
                publisher.publish_noexcept("log", "TYPE_ACCELEROMETER_UNCALIBRATED ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_ACCELEROMETER_UNCALIBRATED ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY) != null){
                publisher.publish_noexcept("log", "TYPE_GRAVITY ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_GRAVITY ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) != null){
                publisher.publish_noexcept("log", "TYPE_GYROSCOPE ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_GYROSCOPE ... Don`t exist. ".getBytes());
            }

            if (mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE_UNCALIBRATED) != null){
                publisher.publish_noexcept("log", "TYPE_GYROSCOPE_UNCALIBRATED ... OK".getBytes());
            } else {
                publisher.publish_noexcept("log", "TYPE_GYROSCOPE_UNCALIBRATED ... Don`t exist. ".getBytes());
            }

            sAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            sGyr = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
            sMag = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);

            mSensorManager.registerListener(listener, sAcc, SensorManager.SENSOR_DELAY_GAME);
            mSensorManager.registerListener(listener, sGyr, SensorManager.SENSOR_DELAY_GAME);
            mSensorManager.registerListener(listener, sMag, SensorManager.SENSOR_DELAY_GAME);
        }
    }

    class CallbackObject implements ISubscribeHandler
    {
        @Override
        public void newmessage(String theme, byte data[])
        {

        }
    }

    SharedPreferences sp;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //publisher = new CrowPublisher(".12.192.168.1.93:10009", new CallbackObject());
        publisher = new TcpPublisher(new CallbackObject());

        hthr = new PublishThread();
        ithr = new ImuThread();
        ithr.start();
        hthr.start();

        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        publisher.ma = this;

        CSquare sqr = (CSquare) findViewById(R.id.sqr);
        sqr.publisher = publisher;
        sqr.vsl = (Slider) findViewById(R.id.vsl);
        sqr.hsl = (Slider) findViewById(R.id.hsl);

        sp = PreferenceManager.getDefaultSharedPreferences(this);
    }

    @Override
    protected void onResume()
    {
        String ip = sp.getString("ip", "127.0.0.1");
        String port = sp.getString("port", "10010");

        System.out.println(ip);
        System.out.println(port);

        ((TextView)findViewById(R.id.ipstr)).setText(ip);
        ((TextView)findViewById(R.id.portstr)).setText(port);

        super.onResume();
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

    void connectState()
    {
        connectionState = true;
        ((android.widget.Button) findViewById(R.id.connect_disconnect)).setText("disconnect");
    }

    void disconnectState()
    {
        connectionState = false;
        ((android.widget.Button) findViewById(R.id.connect_disconnect)).setText("connect");
    }
}
