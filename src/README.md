Tutorial Project: pzcmdr
========================

The project name "pzcmdr" comes from "Pi Zero Commander".
The project was initiated as a controlling device for waking up and shutting
down all the PCs in our computer room by RFID cards. It has been evolved to
include a serial camera and an LED for additional featues. The development
process is protyping-based. Therefore, the architecture is improved for each
version of prototype. Because this project is released as a tutorial, the
prototypes are also included in the project folder but the documentation is
minimal.


Requirements
------------

### Hardware

*   Raspberry Pi Zero (v1.2)
*   RC522-compatible RFID reader
*   Serial Camera (Adafruit [Miniature TTL Serial JPEG Camera with NTSC Video](https://www.adafruit.com/product/1386))
*   RGB LED (common cathode)

### Software

*   Python 3.5 (in Raspbian stretch)
*   Python Packages
    *   pi-rc522
    *   PyDispatcher
    *   pyserial-asyncio
    *   zbar-py
    *   pillow
    *   qrcode (required if you would like to execute `qrcode_gen.py`)
*   Native Packages
    *   libzbar-dev
    *   libatlas-base-dev

### Application Structure

`main.py` The script to launch the application.

`cmdr/` conatins the modules of the application.

`config/` conatins the configuration files.

`scripts/` contains some helper scripts.

Installation, Configuration, and Execution
------------------------------------------

Simply copy the files in this folder to your installation directory. The target
directory should be readable by the executing user. For security concerns, my
suggestion is to make the configuration files be only readable by the executing
user. The executing user should has the permissin to access GPIO, SPI, and serial
ports for communicating with the hardware components. Please note that the serial
camera access the serial port, you need to disable serial TTY while leaving the
serial support enabled.

If you execute the program as the default user (pi) on the Raspberry Pi, the
application should just work by the command:

    python3 main.py

There are sample configurations in the `config/` directory. You may follow the
sytax (described in the sample files) to setup your configuration files and
start the application similar to this:

    python3 main.py ./config/my_iddb.py ./config/my_cmds.py

By default, the log level is INFO. You may specify the log level in the
environment variable `PZCMDR_LOGLEVEL`. For example,

    PZCMDR_LOGLEVEL=DEBUG python3 main.py

Run-time Control
----------------

The application handles the signals for different purposes:

*   `USR1` is used for reloading configuration files.
*   `USR2` is used for toggling the saving of sensed ID, such as RFID's UID.
*   `TERM` and `INT` are used for terminating the program.

For example, supposed the PID of the program is 7130, you may reload the 
configuration files by the command:

    kill -USR1 7130


