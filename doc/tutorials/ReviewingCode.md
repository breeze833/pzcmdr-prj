Reviewing the Code
==================

The developed prototype was fully functional for the purpose of pzcmdr.
However, it had been evolved for several versions.
Of course, it had been gone through heavy modification.
The quality was likely to be degraded.

To determine the potiential causes of quality degradation, user-verification is effective :grin:.
In addition to performing the usage scenarios by ourselves, we also invited a few non-technical people to use the system.
Great! They successfully triggered some unhandled errors!
So, the revision began....


Camera Resuming Issue
---------------------

During the development, this issue was not discovered.
Sometimes the camera couldn't be resumed to the ready state for capturing an image.
The error is now handled by a loop that keeps resuming until success.


Long QR-Code Scanning
---------------------

Sometimes the system became slow-responding after a QR-Code was provided.
It could be a problem of long scanning process.
The `zbar.Scanner().scan()` call is wrapped in an executor to avoid blocking.


Revising the ID Lookup
----------------------

The UID and QR-Code lookup tables were implemented as dictionaries in the modules files.
Hence the reloading function was done by the `importlib.reload()`.
This approach implies that the configuration data are defined as the application code.
It is better to separate the code and the data for maintenance concerns.

We resolved this issue by using the `exec()` function.
It reads the code (script) and exceute the code.
While execution, the global/local environments can be supplied as two dictionaries.
If not supplied, the current run-time is used.
The trick is to use the supplied local environment to hold the execution result.

    globals = {}
    locals = {}
    exec(open('script_file.py').read(), globals, locals)

A script-created identifier can be accessed by `locals['identifier']`.
Therefore, the ID and command configurations are not loaded as modules.
They are loaded as scripts, and pass the lookup tables to the corresponding processing components.


Errors from the External Commands
---------------------------------

Sometimes executing an external command would fail.
The exceptions related to the failure are also emitted to the log.
We changed to logging parameters to log the exceptions only in the debug level:

    logging.warning('warning message')
    logging.debug('debug message', exc_info=True)

The `exc_info=True` specifies that the exception stacktraces are include as part of the logging message.


Summary
-------

No new functionality is introduced in this prototype.
Only the improvements are applied to the code.
