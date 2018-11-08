Attaching the LED Indicator
===========================

The RFID and camera were integrated in pzcmdr.
We discovered an minor issue.
Although the logging messages showed the activities of the application, there was no clue on the deployed system.
Therefore, an indicator to notify the user important activities is required.
In this prototype, an LED was used for the purpose.

LED Indicator
-------------

Comparing to the RFID and the camera components, the LED component is simple to implement.
We took an LED and quickly implemented the functionality.
Whenever a *got_uid* or *got_qrcode* is received, it turns on the LED for one second.
The wiring of the component is

 LED | Pi Zero Pin
:---:|:----------:
 \+  | 13
 \-  | 14 (GND)

It requires the GPIO setup and control

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.OUT)

By setting the output value to 1, the LED is turned on.
    
    GPIO.output(13, 1)

On the contrary, setting output to zero turns off the LED.


RGB LED Indicator
-----------------

We decided to attach an RGB LED to Pi Zero to enable multi-color notification.
The RGB LED we have is the common cathode type.
In otherwords, it integrates R, G, and B LEDs in one package and share the ground pin.
The LED is wired as follows:

 RGB LED | Pi Zero Pin
 :------:|:----------:
  R      | 11
  G      | 13
  B      | 15
  \-      | 14 (GND)

The pin 11, 13, and 15 should be setup as output pins.

Multi-color Indicator
---------------------

We decided to demonstrate the multi-color indicator for errors (red) and command execution (green).
Therefore, new signal *got_error* were defined. 
The application publishes the signal whenever an error occurs.
The indicator listens to *got_error* and *got_cmd* and calls the corresponding color-notification fucntions.


Summary
-------

This is a quick prototyping evolution for improving the user-interface.
It requires the basic knowledge about GPIO control and LED pins.
