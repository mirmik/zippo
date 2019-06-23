package atom.mirmik.zippo_controller;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.*;
import java.io.*;

public class TcpPublisher extends Publisher
{
    Socket sock = null;
    MainActivity ma;

    public void publish(String theme, byte[] data) throws IOException
    {
        if (sock == null)
            return;

        int msglen = theme.length() + data.length + 2 + 6 + 1;
        byte[] msg = new byte[msglen];

        String thmlen_format = String.format("%02d", theme.length());
        String datalen_format = String.format("%06d", data.length);

        msg[0] = 'p';
        System.arraycopy(thmlen_format.getBytes(), 0, msg, 1, 2);
        System.arraycopy(theme.getBytes(), 0, msg, 1 + 2, theme.length());
        System.arraycopy(datalen_format.getBytes(), 0, msg, 1 + 2 + theme.length(), 6);
        System.arraycopy(data, 0, msg, 1 + 2 + theme.length() + 6, data.length);

        OutputStream strm = sock.getOutputStream();

        try {
            strm.write(msg);
        }

        catch (IOException ex)
        {
            sock.close();
            throw ex;
        }
    }

    public void subscribe(String theme)
    {

    }

    TcpPublisher(ISubscribeHandler callback)
    {
        super(callback);
    }

    TcpPublisher(String ip, int port, ISubscribeHandler callback)
    {
        this(callback);

        try {
            connect(ip, port);
        }

        catch (IOException ex)
        {
            System.out.println(String.format("Warn: IOException on socket creating: %s", ex.toString()));
        }
    }

    void connect(String ip, int port) throws IOException
    {
        if (sock != null)
        {
            disconnect();
            sock = null;
        }

        sock = new Socket();
        sock.connect(new InetSocketAddress(ip, port));

        ma.connectState();
    }

    void disconnect()
    {
        try {
            sock.close();
        }

        catch (IOException ex)
        {
            System.out.println(String.format("Warn: IOException on socket clossing: %s", ex.toString()));
        }

        ma.disconnectState();
    }
}
