from pydispatch import dispatcher
import logging
import signal
import os
import asyncio
import functools
from cmdr import RC522
from cmdr import VC0706
from cmdr import UID2Cmd
from cmdr import QRCode2Cmd
from cmdr import UIDLogger
from cmdr import ImageScanner
#from cmdr import TrustedCmdExec
from cmdr import TestCmdExec

class SysSigHandler:
    def __init__(self):
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, functools.partial(self.exit_gracefully))
        loop.add_signal_handler(signal.SIGINT, functools.partial(self.exit_gracefully))
        loop.add_signal_handler(signal.SIGUSR1, functools.partial(self.reload))
        loop.add_signal_handler(signal.SIGUSR2, functools.partial(self.toggle_leak_uid))
        loop.add_signal_handler(signal.SIGCHLD, functools.partial(self.child_exit))
    def exit_gracefully(self):
        logging.debug('cancelling tasks...')
        [task.cancel() for task in asyncio.Task.all_tasks()]
        asyncio.get_event_loop().stop()
    def reload(self):
        dispatcher.send("reload")
    def toggle_leak_uid(self):
        dispatcher.send("toggle_leak_uid")
    def child_exit(self):
        logging.debug('child process exit')
        os.waitpid(0, 0)

def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()

    sig_handlers = SysSigHandler()

    rfid_reader = RC522()
    serial_camera = VC0706()
    uid2cmd = UID2Cmd()
    qrcode2cmd = QRCode2Cmd()
    uid_logger = UIDLogger()
    image_scanner = ImageScanner()
    #trusted_cmd_exec = TrustedCmdExec()
    test_cmd_exec = TestCmdExec()

    dispatcher.send("start_rfid_reader")
    dispatcher.send("start_capture")

    try:
        loop.run_forever()
    finally:
        logging.debug('waiting for all tasks done...')
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True))
        loop.close()

if __name__=='__main__':
    main()
