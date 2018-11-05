import serial
import sys

res = { 'VGA':bytearray([0x00]), 'QVGA':bytearray([0x11]), 'QQVGA':bytearray([0x22]) }

res_get_cmd = bytes([0x56, 0x00, 0x30, 0x04, 0x04, 0x01, 0x00, 0x19])
res_get_ack = bytes([0x76, 0x00, 0x30, 0x00])

res_set_cmd_prefix = bytearray([0x56, 0x00, 0x31, 0x05, 0x04, 0x01, 0x00, 0x19])
res_set_ack = bytes([0x76, 0x00, 0x31, 0x00])

reset_cmd = bytes([0x56, 0x00, 0x26, 0x00])

def set_res(ser_port, res_name):
    ser_port.write(res_get_cmd)
    ser_port.flush()
    reply = ser_port.read(100)
    ser_port.reset_input_buffer()
    ser_port.reset_output_buffer()
    cur_res = None
    if reply[:4]==res_get_ack:
        if reply[5]==0x00:
            cur_res = 'VGA'
        elif reply[5]==0x11:
            cur_res = 'QVGA'
        elif reply[5]==0x22:
            cur_res = 'QQVGA'
        else:
            cur_res = 'Unkown'
    print('Current resolution is {cur_res}'.format(cur_res=cur_res))

    res_set_cmd = res_set_cmd_prefix + res[res_name]
    ser_port.write(res_set_cmd)
    ser_port.flush()
    reply = ser_port.read(100)
    ser_port.reset_input_buffer()
    ser_port.reset_output_buffer()
    if reply[:4]==res_set_ack:
        print('Resolution set to {res_name}'.format(res_name=res_name))
        ser_port.write(reset_cmd)
        ser_port.flush()
        reply = ser_port.read(100)
        return True
    else:
        return False

if __name__=='__main__':
    port = '/dev/ttyAMA0'
    res_name = 'QVGA'
    if len(sys.argv)==2:
        res_name = sys.argv[1]
    elif len(sys.argv)==3:
        port = sys.argv[1]
        res_name = sys.argv[2]
    print('serial port: {port}'.format(port=port))
    print('target resolution: {res_name}'.format(res_name=res_name))
    ser_port = serial.Serial(port, baudrate=38400, timeout=5)
    #ser_port = serial.serial_for_url(url='spy://{port}?file=debug.log'.format(port=port), baudrate=38400, timeout=5)
    
    if set_res(ser_port, res_name):
        print('done')
    else:
        print('failed')

    ser_port.close()
