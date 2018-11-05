import serial
import sys

baudrate_cmd_prefix = bytearray([0x56, 0x00, 0x24, 0x03, 0x01])
baudrate_cmd_code = {
    9600: bytearray([0xAE, 0xC8]),
    19200: bytearray([0x56, 0xE4]),
    38400: bytearray([0x2A, 0xF2]),
    57600: bytearray([0x1C, 0x4C]),
    115200: bytearray([0x0d, 0xA6])
}
baudrate_ack = bytes([0x76, 0x00, 0x24, 0x00])

get_version_cmd = bytes([0x56, 0x00, 0x11, 0x00])
get_version_ack = bytes([0x76, 0x00, 0x11, 0x00])

def set_speed(ser_port, cur_baud, target_baud):
    result = False
    ser_port.baudrate = cur_baud
    ser_port.write(get_version_cmd)
    ser_port.flush()
    reply = ser_port.read(len(get_version_ack))
    ser_port.reset_input_buffer()
    ser_port.reset_output_buffer()
    if reply == get_version_ack:
        print('connected')
        if cur_baud==target_baud:
            return True
        ser_port.write(baudrate_cmd_prefix + baudrate_cmd_code[target_baud])
        ser_port.flush()
        reply = ser_port.read(len(baudrate_ack))
        ser_port.reset_input_buffer()
        ser_port.reset_output_buffer()
        print('set baudrate: {r}'.format(r=target_baud))
        result = True if reply==baudrate_ack else False
    return result

if __name__=='__main__':
    port = '/dev/ttyAMA0'
    target_baud = 115200
    if len(sys.argv)==2:
        target_baud = int(sys.argv[1])
    elif len(sys.argv)==3:
        port = sys.argv[1]
        target_baud = int(sys.argv[2])
    print('serial port: {port}'.format(port=port))
    print('target baudrate: {target_baud}'.format(target_baud=target_baud))
    ser_port = serial.Serial(port, timeout=5)
    #ser_port = serial.serial_for_url(url='spy://{port}?file=debug.log'.format(port=port), timeout=5)

    cur_baud = 38400
    print('Try to connect using {rate}'.format(rate=cur_baud))
    if set_speed(ser_port, cur_baud, target_baud):
        print('done')
    else:
        print('failed')

    ser_port.close()
