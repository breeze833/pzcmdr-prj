The Story
=========

We have a first-generation Raspberry Pi Zero (v1.2).
It features the compact form factor and the very low power consumption.
With only the basic Raspbian running, it can be powered up from the **PWR** port or the **USB** port.
The **USB** port is working in the **gadget mode** instead of the popular **host mode**.
In other words, Pi Zero apears as an USB peripheral device.
Thus, we can configure Pi Zero to be various kinds of devices:
serial, keyboard, mouse, ethernet, video, storage, etc.
If configured as an ethernet device, it emulates the network link over the USB cable.
This establishes a connection between the host computer and Pi Zero.

The gadget mode is interesting in that the Pi Zero could be a software-defined intelligent device.
However, v1.2 does not have builtin camera and network interface.
For the sensing and controlling applications via GPIO, it does not distinguishes itself from Arduino-based solution.
(Of course we know that it is application-dependent. Please don't argue at this point.)

The Pi Zero had been rested in the box for a long time until we encounter the problem to solve....

We have a computer room of 40 computers.
Thanks the [DRBL](https://drbl.org) and the [epoptes](http://www.epoptes.org) for the utilities, we can manage the computers with a few simple commands.
However, we have the requests for issuing wakeup/shutdown commands without logging into the teacher's computer or the DRBL server.
The general solution is to have a device sensing an identification, such as an RFID tag or a QR-Code.
The IDs and the commands are configured by the administrator as the trusted entities within the computer room.
If the ID is associated with a command, the device sends a contolling message to the target system for executing the command.

There are various approaches to implement the solution.
We choose Pi Zero to implement the smart device because of the following reasons:

* The hardware and software are installed in one device.
* The device can be plugged into any one of the computers in the lab.
* It could work stand-alone.
* If network connection is required, we can configure the host interface to match differnt policies.

And, the most important reason is that *we would like to make our Pi Zero contribute to a project*.

