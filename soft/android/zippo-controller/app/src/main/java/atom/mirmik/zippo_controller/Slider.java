package atom.mirmik.zippo_controller;

import android.graphics.*;
import android.view.*;
import android.util.*;
import android.content.*;

public class Slider extends View
{
    public Slider(Context context, AttributeSet attrs)
    {
        super(context, attrs);
    }

    double f = 0.5;

    @Override
    public void onDraw(Canvas canvas)
    {
        int x = getWidth() / 2;
        int y = getHeight() / 2;
        int radius = 20;

        boolean isX = x > y;

        if (isX)
        {
            x = (int)(getWidth() * f);
        }
        else
        {
            y = (int)(getHeight() * f);
        }

        Paint paint = new Paint();

        paint.setColor(Color.parseColor("#ff00ff"));
        canvas.drawCircle(x,y,radius,paint);
    }

    void setPosition(double f)
    {
        this.f = f;
        invalidate();
    }

}
