# This is the configuration file for valid RFID UIDs and QR-Codes

# The UID lookup table
# The key is a tuple representing the UID.
# The value is a tuple. The first is the command ID and the second is the comment.
uids = {
        (166, 29, 34, 126, 231): ('test_python_print', 'Feng-Cheng Chang keyring'),
        (193, 95, 70, 213, 13) : ('test_shell_print', 'Feng-Cheng Chang whitecard'),
}

# The QR-Code lookup table
# The key is a byte sequence which is the decoded data.
# The value is a tuple. The first is the command ID and the second is the comment.
qrcodes = {
        b'this is a test message': ('test_python_print', 'Test QR-Code'),
        b'827fa78f7814021e253b31697137de10': ('toggle_volumio', 'qr_volumio.jpg'),
}
