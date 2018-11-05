Prototypes
==========

01-pzcmdr
---------

RC522 is attached to the Pi Zero. The program loops for sensing an RFID tag
using the examples provided by `pi-rc522`. The following signals are handled:
*   `TERM` and `INT` handle normal kill and Ctrl-C key stroke.
*   `USR1` handles configuration reloading (importlib)
*   `USR2` handles UID saving to a file that is only readable by the executing user.
*   `CHLD` handles the termination of a child process.

02-pzcmdr-async
---------------

Based on the prototype 01, develop the asyncio implementation. Wrap the blocking call
in `loop.run_in_executor()` and properly resolve the issue that we need to interrupt
executor when application shutdown.

03-pzcmdr-dispatcher
--------------------

Based on the prototype 02, redesign the architecture to use PyDispatcher. The publisher-subscriber
pattern allow us to decouple the components by using software events (PyDispatcher
 signals). The package structure is reorganized to source (cmdsrc), processing
 (cmdproc), and destination (cmddst).

04-pzcmdr-cam
-------------

Based on prototype 03, include the serial camera component. The program periodically
asks the camera to capture a frame, gets the frame as JPEG, decodes JPEG using PIL,
and scans for QR-Codes. The pyserial-asyncio is also used for async I/O with the camera.
The high-level Stream reader/writer is used for communication.

05-pzcmdr-led
-------------

Based on prototype 04, include an RGB LED to indicate:
1.  a command ID is determined (green)
1.  an error occurs (red)

06-pzcmdr-review
----------------

Review prototype 05 and improve the design.
*   Replace the `importlib`-based reloading with a generic `exec()`-based solution.
    With the new design, the configuration file is not a module and thus can be separated
    from the package files.
*   Due to the above improvement, the command executor is object-based, not class-based.
*   Put the QR-Code scanning process in an executor thread.
*   Make the log level configurable from environment variable.

