package atom.mirmik.zippo_controller;

import android.graphics.*;
import android.os.AsyncTask;
import android.view.*;
import android.util.*;
import android.content.*;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class CSquare extends View
{
    Publisher publisher;
    Slider vsl;
    Slider hsl;

    public CSquare(Context context, AttributeSet attrs)
    {
        super(context, attrs);
    }

    @Override
    public void onDraw(Canvas canvas)
    {
        int x = getWidth();
        int y = getHeight();
        int c = 3;

        Paint paint = new Paint();

        paint.setColor(Color.parseColor("#000000"));
        canvas.drawRect(0,0, x, y, paint);
        paint.setColor(Color.parseColor("#FFFFFF"));
        canvas.drawRect(c,c, x-c, y-c, paint);
    }

    @Override
    public boolean onTouchEvent(android.view.MotionEvent ev)
    {
        float x = ev.getX();
        float y = ev.getY();
        if (x > getWidth()) x = getWidth();
        if (y > getHeight()) y = getHeight();
        if (x < 0) x = 0;
        if (y < 0) y = 0;

        x = x / getWidth();
        y = y / getHeight();

        System.out.println(x);
        System.out.println(y);

        hsl.setPosition(x);
        vsl.setPosition(y);

        final float fx = (float)x;
        final float fy = (float)y;

        AsyncTask.execute(new Runnable() {
            @Override
            public void run() {
                publisher.publish_noexcept("zippo_shor", ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putFloat((float) fx).array());
                publisher.publish_noexcept("zippo_sver", ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putFloat((float) fy).array());
            }
        });

        return true;
    }
}
