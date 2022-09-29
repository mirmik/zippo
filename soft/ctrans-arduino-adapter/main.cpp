#include <crow/address.h>
#include <crow/gates/udpgate.h>
#include <crow/nodes/subscriber_node.h>
#include <igris/buffer.h>
#include <igris/protocols/gstuff.h>
#include <nos/io/serial_port.h>

nos::serial_port serial;

void subscribe_handler(igris::buffer msg)
{
    auto gmsg = gstuffing(msg);
    serial.write(gmsg.data(), gmsg.size());
    serial.flush();

    nos::print_dump(gmsg.data(), gmsg.size());
}

crow::subscriber_node subscriber(subscribe_handler);

int main()
{
    crow::create_udpgate(12);
    crow::start_spin();
    subscriber.init_subscribe(crow::crowker_address(),
                              CROWKER_SERVICE_BROCKER_NODE_NO,
                              "zippo/ctr",
                              0,
                              0,
                              0,
                              0);
    subscriber.bind();
    subscriber.install_keepalive(2000);

    serial.open("/dev/ttyACM0", 115200, 'n', 1, 1);

    while (1)
    {
        char c;
        serial.read(&c, 1);
        nos::print((int)c, " ");
        nos::write(&c, 1);
        nos::println();
    }
}