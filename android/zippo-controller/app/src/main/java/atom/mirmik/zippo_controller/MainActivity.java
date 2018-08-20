package atom.mirmik.zippo_controller;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    Publisher publisher;
    Thread thr;

    public class PublishThread extends Thread {
        int i = 0;
        public void run(){
            while(true) {
                publisher.publish("hello", String.format("HelloWorld %d", i++).getBytes());
                try {
                    Thread.sleep(1000);
                }catch (Exception e) {}
            }
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        publisher = new Publisher();
        publisher.setHostAddress(".12.192.168.1.135:10009");

        //publisher.publish("hello", String.format("HelloWorld").getBytes());

        thr = new PublishThread();
        thr.start();

        setContentView(R.layout.activity_main);
    }


}
