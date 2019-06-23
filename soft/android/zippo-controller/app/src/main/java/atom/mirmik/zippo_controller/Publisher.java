package atom.mirmik.zippo_controller;

import java.io.IOException;

interface ISubscribeHandler
{
    void newmessage(String theme, byte[] data);
}

public abstract class Publisher
{
    public abstract void publish(String theme, byte[] data) throws IOException;
    public abstract void subscribe(String theme);

    ISubscribeHandler callback;

    public void publish(String theme, String data) throws IOException
    {
        publish(theme, data.getBytes());
    }

    public void publish_noexcept(String theme, String data)
    {
        publish_noexcept(theme, data.getBytes());
    }

    public void publish_noexcept(String theme, byte[] data)
    {
        try
        {
            publish(theme, data);
        }

        catch (IOException ex)
        {
            //pass
        }
    }

    Publisher(ISubscribeHandler callback)
    {
        this.callback = callback;
    }
}