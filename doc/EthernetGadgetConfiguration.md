Ethernet Gadget Configuration
=============================

Raspberry Pi Zero supports the gadget mode and emulates various devices.
To enable it acts like an ethernet device and communicates with the host computer,
there are configuration files to modify. I have experienced a few network
configurations. Here are my procedures for them.

Enable the Ethernet Gadget Mode
-------------------------------

To enable the ethernet gadget, you need to mount the first partition of the Raspbian
image and make sure that the `config.txt` includes a line

    dtoverlay=dwc2

Then, if you can access the second partition:

*   modify `etc/modules` to include `dwc2` and `g_ether` module
*   create `etc/modprobe.d/gether.conf` and add the line
        options g_ether dev_addr=<dev_addr> host_addr=<host_addr>
    *    where `dev_addr` is the MAC address on the Pi Zero interface (usb0)
         and `host_addr` is the MAC address on the host interface (interface name may vary)
    *    If the addresses are fixed, it is likely to get the same IP from DHCP.

If you cannot access the second partition, simply boot into the system and modify
`/etc/modules` and `/etc/modprobe.d/g_ether.conf` accordingly.

If there is no peripherals attached to Pi Zero, connect the gadget USB port to the host
and the power from the gadget USB port is enough for booting the system. If the power is
low,
*    you may prepare an additional USB cable and connect the power port to a power adapter;
*    or prepare a powered USB hub and connect the gadget port to the host via the hub.

If it works properly, you will see a new network interface on the host. To determine the
interface, either use

    ifconfig -a

or

    ip link

With the ethernet-over-USB, you can imagine that there is a ethernet cable between the host
and the Pi Zero. On the Pi Zero side, the interface is `usb0`. On the host side, the interface
is the one determined by `ifconfig -a` or `ip link`. In the following sections, we call it
`<pi0intf>`

Pi Zero is Connected to a Host Bridge
-------------------------------------

Now, let's consider the case that the host has a bridge called `br0`. The procedure to add
the Pi Zero to the bridge is listed below.

1. `brctl addif br0 <pi0intf>`
2. `ip link set <pi0intf> up`

The Pi Zero will get an IP from the DHCP if available.

Pi Zero is Connected Directly to the Host Only
----------------------------------------------

In this configuration, we only allow communications between the host and the Pi Zero.
The suggested approach is to configure both interfaces with fixed IP addresses.

On the Pi Zero:

*    edit `/etc/dhcpcd.conf` to include the following static configuration

          interface usb0
          fallback static_usb0

          profile static_usb0
          static ip_address=10.1.1.100/24
          static routers=10.1.1.1

On the host:

*    depending on the configuration tool used, you may need to modify `/etc/dhcpcd.conf`
     or `/etc/network/interfaces`
*    configure `<pi0intf>` to the static IP 10.1.1.1


Pi Zero is Connected to the Internet via the Host
-------------------------------------------------

If you would like to allow the Pi Zero to access the Internet via the host,
IP forwarding and NAT rules should be enabled.

On the Pi Zero:

*   follow the instructions in the previous configuration
*   add the DNS setup to the profile:
        static domain_name_servers=8.8.8.8

On the host:

*   follow the instructions in the prevuous configuration
*   make sure that `sysctl` enables `net.ipv4.ip_forward=1`
    *    apply to run-time by executing the `sysctl` program
    *    enable on each boot by modifying `/etc/sysctl.conf`
         or one of the files in `/etc/sysctl.d`
*   enable the firewall rule
        iptables -t nat -A POSTROUTING -s 10.1.1.100 -j MASQUERADE

You may consider to hook the `iptables` command to the network configuration
process so that it is executed automatically.
