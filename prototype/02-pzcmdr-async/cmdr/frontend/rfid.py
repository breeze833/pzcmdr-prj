from pirc522 import RFID
import logging
import os
import asyncio

class RFIDFrontend:
    def __init__(self, cmdexec, uid_db):
        """
        Initialize an RFID frontend to trigger the trusted command executor.

        Arguments:
        loop -- The event loop.
        uid_db -- The dictionary that associates an UID to the trusted command ID.
        cmdexec -- The backend trusted command executor.
        """
        self.need_leak_uid = False
        self.uid_db = uid_db
        self.cmdexec = cmdexec
        self.is_running = None

    async def handle_tag_cmd(self, uid):
        try:
            cmd_id = self.uid_db[tuple(uid)][0]
            if cmd_id:
                await self.cmdexec.run(cmd_id)
        except asyncio.CancelledError:
            raise
        except KeyError:
            logging.warning('UID not found')

    def leak_uid(self, uid):
        if self.need_leak_uid:
            fd = os.open('leak_uid.txt', os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'w') as f:
                f.write(str(uid))
            self.need_leak_uid = False

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
                self.leak_uid(uid)
                await self.handle_tag_cmd(uid)
        logging.debug('finish reading...')

    async def start_reader(self):
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

    def stop_reader(self):
        if self.is_running:
            logging.info('stopping RFID reader...')
            self.is_running = False
            self.rdr.cleanup()

