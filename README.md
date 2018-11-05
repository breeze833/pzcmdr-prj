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
*   Native Packages
    *   libzbar-dev
    *   libatlas-base-dev

Project Organization
--------------------
`doc/` contains the documents

`prototype/` contains the prototypes developed prior to the released version

`src/` contains the released version


