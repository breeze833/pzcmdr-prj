import logging
import signal
import os
import importlib
import tagdb
from cmdr import RFIDFrontend
from cmdr import CmdExec
from trusted_cmds import trusted_commands

class SysSigHandler:
    def __init__(self, rfid_frontend):
        self.rfid_frontend = rfid_frontend
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGUSR1, self.reload_tagdb)
        signal.signal(signal.SIGUSR2, self.leak_next_uid)
        signal.signal(signal.SIGCHLD, self.child_exit)
    def exit_gracefully(self, signo, frame):
        logging.info('stopping RFID reader loop...')
        exit()
    def reload_tagdb(self, signo, frame):
        logging.info('reloading tags...')
        importlib.reload(tagdb)
        self.rfid_frontend.uid_db = tagdb.uids
    def leak_next_uid(self, signo, frame):
        self.rfid_frontend.leak_uid = True
    def child_exit(self, signo, frame):
        logging.debug('child process exit')
        os.waitpid(0, 0)


if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    cmdexec = CmdExec(trusted_commands)
    rfid_frontend = RFIDFrontend(cmdexec, tagdb.uids)
    sig_handler = SysSigHandler(rfid_frontend)
    rfid_frontend.reader_loop()
