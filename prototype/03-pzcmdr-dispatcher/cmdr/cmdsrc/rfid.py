from pirc522 import RFID
from pydispatch import dispatcher
import logging
import asyncio

class RFIDFrontend:
    """
    The RFID frontend that triggers the command execution when a card is ready.
    The UID will be sent with a signal "got_uid".

    The signals "start_rfid_reader" and "stop_rfid_reader" are used
    for controlling the reader.
    """

    def __init__(self):
        """
        Initialize an RFID frontend to trigger the trusted command executor.
        """
        self.need_leak_uid = False
        self.is_running = None
        dispatcher.connect(self.start_reader, signal='start_rfid_reader')
        dispatcher.connect(self.stop_reader, signal='stop_rfid_reader')

    async def read(self):
        logging.debug("waiting for tag...")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.rdr.wait_for_tag)
        (error, tag_type) = self.rdr.request()
        if not error:
            logging.debug("Tag detected")
            (error, uid) = self.rdr.anticoll()
            if not error:
                logging.debug("UID: " + str(uid))
                dispatcher.send("got_uid", self, tuple(uid))
        logging.debug('finish reading...')

    async def _start_reader(self):
        try:
            logging.info("starting RFID reader...")
            self.rdr = RFID(speed=500000)
            self.is_running = True
            while self.is_running:
                await self.read()
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            self.rdr.irq.set() # This is used for exiting the blocking state of wait_for_tag()
            self.stop_reader()
            raise
        except Exception as e:
            logging.warning('Unexprected exception....')
            logging.debug(e)
        finally:
            self.stop_reader()

    def start_reader(self):
        asyncio.ensure_future(self._start_reader())

    def stop_reader(self):
        if self.is_running:
            logging.info('stopping RFID reader...')
            self.is_running = False
            self.rdr.cleanup()

