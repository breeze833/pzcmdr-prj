Attaching RC522 to Pi Zero and Sensing the Tags
===============================================

The RC522 is popular in many RFID related projects.
According to the [pi-rc522](https://github.com/ondryaso/pi-rc522), we connect our RC522 module to Pi Zero as follows:

RC522 Pin | Pi Zero Pin
:--------:|:----------:
 VCC      | 17
 RST      | 22
 GND      | 20
 MISO     | 21
 MOSI     | 19
 SCK      | 23
 NSS      | 24
 IRQ      | 18

Installing the package is easy by

    pip install pi-rc522 (for Python 2)

or
    pip3 install pi-rc522 (for Python 3)

Copy the sample code, save it to a script file, and execute it to experiment with it.
The result is encouraging because we make the RFID reader sensing tags with only a few lines of code.
Then, we pressed `Ctrl-C` to terminate the program and restarted the program.
We noticed some extra messages related to GPIO resources. Apparently the cleanup routine was not properly finished.
