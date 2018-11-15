The Defined PyDispatcher Signals Used in pzcmdr
===============================================

| Siganl | Purpose | Sender | Receiver |
|:-------|:--------|:-------|:---------|
|`start`| Start the entry servcie components | the run() in App | RC522, VC0706 |
|`stop`| Stop the service components | currently no sender | RC522, VC0706 |
|`captured_jpeg`| A JPEG image is captured | VC0706 | JPEG2Image |
|`got_uid`| An UID is sensed | RC522 | LED, UID2Cmd, UIDLogger |
|`got_qrcode`| A QR-Code is scanned | QRCodeScanner | LED, QRCode2Cmd  |
|`got_cmd`| A command is determined | QRCode2Cmd, UID2Cmd | CmdExec, RGB_LED |
|`reload`| Reload the configuration with the given data | USR1 signal handler in App | CmdExec, QRCode2Cmd, UID2Cmd |
|`got_error`| An error occurs | QRCode2Cmd, UID2Cmd | RGB_LED |
|`toggle_leak_uid`| Toggle the logging of UIDs | USR2 signal handler in App | UIDLogger |
|`got_image`| An PIL Image object is ready| JPEG2Image | Image2Gray |
|`got_gray`| An PIL gray-level Image object is ready | Image2Gray | QRCodeScanner |
