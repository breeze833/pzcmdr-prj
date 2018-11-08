The Defined PyDispatcher Signals Used in pzcmdr
===============================================

| Siganl | Purpose | Sender | Receiver |
|:-------|:--------|:-------|:---------|
|`start`| Start the entry servcie components | the main thread | RC522, VC0706 |
|`stop`| Stop the service components | currently no sender | RC522, VC0706 |
|`captured_image`| An image is captured | VC0706 | ImageScanner |
|`got_uid`| An UID is sensed | RC522 | LED, UID2Cmd, UIDLogger |
|`got_qrcode`| A QR-Code is scanned | ImageScanner | LED, QRCode2Cmd  |
|`got_cmd`| A command is determined | QRCode2Cmd, UID2Cmd | CmdExec, RGB_LED |
|`reload`| Reload the configuration with the given data | the signal handler | CmdExec, QRCode2Cmd, UID2Cmd |
|`got_error`| An error occurs | QRCode2Cmd, UID2Cmd | RGB_LED |
|`toggle_leak_uid`| Toggle the logging of UIDs | the signal handler | UIDLogger |
