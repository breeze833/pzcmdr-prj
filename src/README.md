Source Code for pzcmdr
======================

The project name "pzcmdr" comes from "Pi Zero Commander".
The project was initiated as a controlling device for waking up and shutting
down all the PCs in our computer room by RFID cards. It has been evolved to
include a serial camera and an LED for additional featues.
The architecture is designed to be flexible to include new processing components.
It may be adapted or ported to some other environment.


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
==========================================

Please refer to the `Setup.md` in the project `doc/` folder for deatils.
