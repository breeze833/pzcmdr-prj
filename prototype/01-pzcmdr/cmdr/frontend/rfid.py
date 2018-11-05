from pirc522 import RFID
import logging
import time
import os


class RFIDFrontend:
    def __init__(self, cmdexec, uid_db):
        """
        Initialize an RFID frontend to trigger the trusted command executor.

        Arguments:
        uid_db -- The dictionary that associates an UID to the trusted command ID.
        cmdexec -- The backend trusted command executor.
        """
        self.need_leak_uid = False
        self.uid_db = uid_db
        self.cmdexec = cmdexec

    def handle_tag_cmd(self, uid):
        try:
            cmd_id = self.uid_db[tuple(uid)][0]
            if cmd_id:
                self.cmdexec.run(cmd_id)
        except KeyError:
            logging.warning('UID not found')

    def leak_uid(self, uid):
        if self.need_leak_uid:
            fd = os.open('leak_uid.txt', os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'w') as f:
                f.write(str(uid))
            self.need_leak_uid = False

    def reader_loop(self):
        try:
            rdr = RFID(speed=500000)
            logging.info("starting RFID reader loop...")
            
            while True:
                logging.debug("waiting for tag...")
                rdr.wait_for_tag()
                (error, tag_type) = rdr.request()
                if not error:
                    logging.debug("Tag detected")
                    (error, uid) = rdr.anticoll()
                    if not error:
                        logging.debug("UID: " + str(uid))
                        self.leak_uid(uid)
                        self.handle_tag_cmd(uid)
                time.sleep(1)
        except SystemExit:
            logging.info('exiting program...')
        except Exception as e:
            logging.warning('Unexprected exception, stopping RFID reader loop....')
            logging.debug(e)
        finally:
            # Calls GPIO cleanup
            rdr.cleanup()

