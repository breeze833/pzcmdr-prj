import serial
import sys

reset_cmd = bytes([0x56, 0x00, 0x26, 0x00])
get_version_cmd = bytes([0x56, 0x00, 0x11, 0x00])
get_version_ack = bytes([0x76, 0x00, 0x11, 0x00])

def is_connected(ser_port, baud):
    ser_port.baudrate = baud
    ser_port.write(get_version_cmd)
    ser_port.flush()
    reply = ser_port.read(len(get_version_ack))
    ser_port.reset_input_buffer()
    ser_port.reset_output_buffer()
    if reply == get_version_ack:
        return True
    else:
        return False

def reset(ser_port):
    ser_port.write(reset_cmd)
    ser_port.flush()
    ser_port.reset_input_buffer()
    ser_port.reset_output_buffer()

if __name__=='__main__':
    port = '/dev/ttyAMA0'
    target_baud = 115200
    if len(sys.argv)==2:
        port = sys.argv[1]
    print('serial port: {port}'.format(port=port))
    ser_port = serial.Serial(port, timeout=5)
   
    for cur_baud in [9600, 19200, 38400, 57600, 115200]:
        print('Try to connect using {rate}'.format(rate=cur_baud))
        if is_connected(ser_port, cur_baud):
            print('resetting...')
            reset(ser_port)
            print('done')
            break
    else:
        print('all failed')

    ser_port.close()
