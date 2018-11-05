import logging
import serial
import serial_asyncio
import asyncio
from pydispatch import dispatcher

baudrate_cmd_prefix = bytearray([0x56, 0x00, 0x24, 0x03, 0x01])
baudrate_cmd_code = {
    9600: bytearray([0xAE, 0xC8]),
    19200: bytearray([0x56, 0xE4]),
    38400: bytearray([0x2A, 0xF2]),
    57600: bytearray([0x1C, 0x4C]),
    115200: bytearray([0x0d, 0xA6])
}
baudrate_ack = bytes([0x76, 0x00, 0x24, 0x00])

reset_cmd = bytes([0x56, 0x00, 0x26, 0x00])

capture_cmd = bytes([0x56, 0x00, 0x36, 0x01, 0x00])
capture_ack = bytes([0x76, 0x00, 0x36, 0x00, 0x00])
buflen_cmd = bytes([0x56, 0x00, 0x34, 0x01, 0x00])
buflen_ack = bytes([0x76, 0x00, 0x34, 0x00, 0x04])
bufread_cmd_prefix = bytes([0x56, 0x00, 0x32, 0x0C, 0x00, 0x0A])
bufread_ack = bytes([0x76, 0x00, 0x32, 0x00, 0x00])
resume_cmd = bytes([0x56, 0x00, 0x36, 0x01, 0x03])
resume_ack = bytes([0x76, 0x00, 0x36, 0x00, 0x00])

class VC0706:
    """
    The class for controlling the serial camera VC0706 to capture images.
    The captured JPEG image will be sent with the signal "captured_image".

    The "start_capture" and "stop_capture" are used for controlling the camera.
    """
    def __init__(self, port='/dev/ttyAMA0', baud=115200):
        self.port = port
        self.baud = baud
        self.is_running = False
        self.reset()
        if self.set_speed():
            logging.info('baudrate changed to {baudrate}'.format(baudrate=self.baud))
        else:
            logging.warning('baudrate change failed')
        dispatcher.connect(self.start_capture, signal='start_capture')
        dispatcher.connect(self.stop_capture, signal='stop_capture')

    def reset(self):
        """
        Reset the camera.
        This operation also reset the serial baudrate to 38400.
        """
        self.serial = serial.Serial(self.port, baudrate=self.baud)
        self.serial.write(reset_cmd)
        self.serial.flush()
        self.serial.close()
        del self.serial

    def set_speed(self):
        """
        Try to set the baudrate for communication.
        We assume that the camera is initially at 38400.
        """
        self.serial = serial.Serial(self.port)
        logging.debug('assuming current baudrate=38400, configuring to {baud}'.format(baud=self.baud))
        self.serial.baudrate = 38400
        baudrate_cmd = baudrate_cmd_prefix + baudrate_cmd_code[self.baud]
        self.serial.write(baudrate_cmd)
        self.serial.flush()
        reply = self.serial.read(len(baudrate_ack))
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        result = True if reply==baudrate_ack else False
        self.serial.close()
        del self.serial
        return result

    async def capture(self):
        """
        Capture a frame and store the JPEG in camera's buffer.
        This operation pause the camera capturing to freeze the image.
        Call resume() to re-activate the capturing process.
        Returns:
            True if the command is successful. Otherwise False.
        """
        self.writer.write(capture_cmd)
        await self.writer.drain()
        reply = await self.reader.read(5)
        return True if reply==capture_ack else False

    async def resume(self):
        """
        Resume the capturing process.
        Returns:
            True if the command is successful. Otherwise False.
        """
        self.writer.write(resume_cmd)
        await self.writer.drain()
        reply = await self.reader.read(5)
        return True if reply==resume_ack else False

    async def get_buffer_len(self):
        """
        Get the data length in the camera's buffer.
        Returns:
            The number of byes. If is is -1, there is something wrong.
        """
        self.writer.write(buflen_cmd)
        await self.writer.drain()
        reply = await self.reader.read(9)
        if len(reply)==9 and reply[:5]==buflen_ack:
            length = (reply[5]<<24) + (reply[6]<<16) + (reply[7]<<8) + reply[8]
            return length
        else:
            return -1

    async def read_buffer_data(self, start_addr, data_len):
        """
        Read data from the camera's buffer.
        According to the specification, the reply data is the buffer data prepended and appended with the ack message.

        Arguments:
        start_addr -- The starting offset of the reading.
        data_len -- The number of bytes to read.
        """
        bufread_cmd = bufread_cmd_prefix + bytearray([(start_addr>>24)&0xFF, (start_addr>>16)&0xFF, (start_addr>>8)&0xFF, start_addr&0xFF])
        bufread_cmd += bytearray([(data_len>>24)&0xFF, (data_len>>16)&0xFF, (data_len>>8)&0xFF, data_len&0xFF])
        bufread_cmd += bytearray([1, 0]) # delay
        self.writer.write(bufread_cmd)
        await self.writer.drain()
        reply = await self.reader.read(5)
        if reply[:5]==bufread_ack:
            data = bytearray([])
            while len(data)<data_len+5:
                data += await self.reader.read(data_len+5)
            return data[:data_len]
        else:
            return None

    async def _start_capture(self, interval):
        try:
            #self.reader, self.writer = await serial_asyncio.open_serial_connection(url='spy://{port}?file=debug.log'.format(port=self.port), baudrate=self.baud)
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baud)
            self.is_running = True
            while self.is_running:
                is_captured = await self.capture()
                if is_captured:
                    data_len = await self.get_buffer_len()
                    if data_len>0:
                        data = await self.read_buffer_data(0, data_len)
                        dispatcher.send('captured_image', self, data)
                is_resumed = await self.resume()
                while not is_resumed:
                    logging.warning('resuming camera failed')
                    await asyncio.sleep(1)
                    is_resumed = await self.resume()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            raise
        finally:
            self.stop_capture()
            await asyncio.sleep(3)
            self.reset()

    def start_capture(self, interval=1):
        """
        Start capturing images.
        There is a guard interval between two image capturing processes.

        Argument:
        interval -- The guard interval in seconds.
        """
        logging.info('starting camera...')
        asyncio.ensure_future(self._start_capture(interval))

    def stop_capture(self):
        """
        Stop the capturing process and reset the camera.
        """
        if self.is_running:
            logging.info('stopping camera...')
            self.is_running = False
            del self.reader
            del self.writer


