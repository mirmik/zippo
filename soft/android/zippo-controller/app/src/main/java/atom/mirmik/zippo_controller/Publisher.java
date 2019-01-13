package atom.mirmik.zippo_controller;

import java.util.*;
import java.net.*;
import java.lang.*;

public class Publisher {
    byte[] haddr;
    DatagramSocket sock;
    SocketAddress sockaddr;

    public Publisher() {
        System.out.println("Publisher created");
        try {
            sock = new DatagramSocket();
            InetAddress iaddr = InetAddress.getByName("192.168.1.145");
            sockaddr = new InetSocketAddress(iaddr, 10009);
        } catch (Exception e) {
            System.out.println(e);
            System.exit(0);
        }
    }

    public static byte[] concat(byte[] a, byte[] b) {
        byte[] c = new byte[a.length + b.length];
        System.arraycopy(a, 0, c, 0, a.length);
        System.arraycopy(b, 0, c, a.length, b.length);
        return c;
    }

    public void publish(String theme, byte[] data) {
        byte[] bytes = new byte[10];
        byte[] addr = new byte[7];
        byte[] sh = new byte[4];
        byte[] thm = theme.getBytes();

        bytes[0] = (byte)0b00100000; //pflag
        bytes[1] = (byte) (bytes.length + addr.length + data.length + thm.length + sh.length); //flen hi
        bytes[2] = 0; //flen lo
        bytes[3] = (byte) addr.length; //alen
        bytes[4] = 0; //stg
        bytes[5] = 0; //ackquant
        bytes[6] = 0; //ackquant
        bytes[7] = 0; //seqid
        bytes[8] = 0; //seqid
        bytes[9] = 0; //qos

        addr[0] = (byte)0x0C;
        addr[1] = (byte)0xC0;
        addr[2] = (byte)0xA8;
        addr[3] = (byte)0x01;
        addr[4] = (byte)0x87;
        addr[5] = (byte)0x27;
        addr[6] = (byte)0x19;

        sh[0] = 1;
        sh[1] = (byte) thm.length;
        sh[2] = (byte) (data.length & 0xFF);
        sh[3] = (byte) ((data.length & 0xFF00) >> 8);

        byte[] packdata = bytes;
        packdata = concat(packdata,addr);
        packdata = concat(packdata,sh);
        packdata = concat(packdata,thm);
        packdata = concat(packdata,data);

        try {
            DatagramPacket packet;
            packet = new DatagramPacket(packdata, packdata.length, sockaddr);
            sock.send(packet);
        }
        catch (Exception e) {
            System.out.println(e);
            System.exit(0);
        }
    }

    public void setHostAddress(String addr) {
        int sz = 0;
        int cursor = 0;
        int retcursor = 0;
        byte[] bytes = addr.getBytes();
        byte[] retaddr = new byte[bytes.length];
        String res;

        while (cursor != bytes.length) {
            switch (bytes[cursor]) {
                case '.':
                    System.out.println("founded .");
                    byte b = 0;
                    try {
                        while(Character.isDigit(bytes[++cursor])) {
                            b *= 10;
                            b += bytes[cursor] - '0';
                        }
                    } catch(Exception e) {}
                    retaddr[++sz] = b;
                    System.out.println(String.format("put 0x%X", b));
                    break;
                case ':':
                    System.out.println("founded :");
                    short bb = 0;
                    try {
                        while(Character.isDigit(bytes[++cursor])) {
                            bb *= 10;
                            bb += bytes[cursor] - '0';
                        }
                    } catch(Exception e) {}
                    retaddr[++sz] = (byte)(bb & 0xFF00 >> 8);
                    retaddr[++sz] = (byte)(bb & 0x00FF);
                    System.out.println(String.format("put 0x%X", bb));
                    break;
                case '#':
                    System.out.println("founded #: TODO");
                    System.exit(-1);
                    break;
                default:
                    System.out.println("founded ???");
                    System.out.println(bytes[cursor]);
                    System.exit(-1);
                    break;
            }
        }

        haddr = Arrays.copyOfRange(retaddr, 0, sz);


        //		case '#': {
        //			uint8_t high;
        //			bool phase = 0;
        //			while(isxdigit(*++it)) {
        //				if (phase) {
        //					*dst++ = (high << 4) | sym2byte(*it);
        //					++sz;
        //				}
        //				else {
        //					high = sym2byte(*it);
        //				}
        //				phase = !phase;
        //			}
        //			if (phase) {
        //				*dst++ = high << 4;
        //				++sz;
        //			}
        //		}

    }
}