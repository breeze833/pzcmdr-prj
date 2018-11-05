import logging
import asyncio
import RPi.GPIO as GPIO
from pydispatch import dispatcher

class LED:
    """
    The LED indicator. It is turn on for one second when an UID or a QR-Code is sensed.
    Therefore, it listens to "got_uid" and "got_qrcode" signals.
    """
    def __init__(self, led_pin=13):
        self.led_pin = led_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.led_pin, GPIO.OUT)
        dispatcher.connect(self.notify, signal='got_uid')
        dispatcher.connect(self.notify, signal='got_qrcode')

    async def _notify(self):
        GPIO.output(self.led_pin, 1)
        await asyncio.sleep(1)
        GPIO.output(self.led_pin, 0)

    def notify(self, _):
        """
        The handler for a sensed UID or QR-Code.
        It only indicates a sensed data is received. Thus, the data object is ignored.
        """
        asyncio.ensure_future(self._notify())

class RGB_LED:
    """
    The RGB LED indicator.
    The implementation is for CC (common cathode) type RGB LED.
    There are generic turn-on methods for colors.
    Only R, G, and B for notifications are implemented.

    The B notification is triggered when "got_uid" or "got_qrcode" is received. (not activated by default)
    The G notofication is triggered when "got_cmd" is received.
    The R notification is triggered when "got_error" is received.
    """
    def __init__(self, red_pin=11, green_pin=13, blue_pin=15, duration=1):
        """
        Initialize the RGB LED indicator.

        Arguments:
        red_pin -- The pin number for red.
        green_pin -- The pin number for green.
        blue_pin -- The pin number for blue.
        duration -- The duration of the indication.
        """
        self.r_pin = red_pin
        self.g_pin = green_pin
        self.b_pin = blue_pin
        self.duration = duration
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.r_pin, GPIO.OUT)
        GPIO.setup(self.g_pin, GPIO.OUT)
        GPIO.setup(self.b_pin, GPIO.OUT)
        #dispatcher.connect(self.blue_notify, signal="got_uid")
        #dispatcher.connect(self.blue_notify, signal="got_qrcode")
        dispatcher.connect(self.green_notify, signal="got_cmd")
        dispatcher.connect(self.red_notify, signal="got_error")

    def red(self):
        GPIO.output(self.r_pin, 1)
        GPIO.output(self.g_pin, 0)
        GPIO.output(self.b_pin, 0)
 
    def green(self):
        GPIO.output(self.r_pin, 0)
        GPIO.output(self.g_pin, 1)
        GPIO.output(self.b_pin, 0)

    def blue(self):
        GPIO.output(self.r_pin, 0)
        GPIO.output(self.g_pin, 0)
        GPIO.output(self.b_pin, 1)

    def yellow(self):
        GPIO.output(self.r_pin, 1)
        GPIO.output(self.g_pin, 1)
        GPIO.output(self.b_pin, 0)
 
    def magenta(self):
        GPIO.output(self.r_pin, 1)
        GPIO.output(self.g_pin, 0)
        GPIO.output(self.b_pin, 1)
 
    def cyan(self):
        GPIO.output(self.r_pin, 0)
        GPIO.output(self.g_pin, 1)
        GPIO.output(self.b_pin, 1)
 
    def white(self):
        GPIO.output(self.r_pin, 1)
        GPIO.output(self.g_pin, 1)
        GPIO.output(self.b_pin, 1)
 
    def black(self):
        GPIO.output(self.r_pin, 0)
        GPIO.output(self.g_pin, 0)
        GPIO.output(self.b_pin, 0)

    async def _red_notify(self):
        self.red()
        await asyncio.sleep(self.duration)
        self.black()

    def red_notify(self, _):
        """
        The handler for an error.
        It only indicates an error is received. Thus, the data object is ignored.
        """
        asyncio.ensure_future(self._red_notify())

    async def _green_notify(self):
        self.green()
        await asyncio.sleep(self.duration)
        self.black()

    def green_notify(self, _):
        """
        The handler for a command execution.
        It only indicates the execution is started. Thus, the data object is ignored.
        """
        asyncio.ensure_future(self._green_notify())

    async def _blue_notify(self):
        self.blue()
        await asyncio.sleep(self.duration)
        self.black()

    def blue_notify(self, _):
        """
        The handler for a sensed UID or QR-Code.
        It only indicates a sensed data is received. Thus, the data object is ignored.
        """
        asyncio.ensure_future(self._blue_notify())

