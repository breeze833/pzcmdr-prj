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
:--:|:----------:
  \+| 13
  \-| 14

It requires the GPIO setup and control

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13, GPIO.OUT)

By setting the output value to 1, the LED is turned on.
    
    GPIO.output(13, 1)

On the contrary, setting output to zero turns off the LED.


RGB LED Indicator
-----------------

