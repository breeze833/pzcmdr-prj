import logging
import signal
import os
import importlib
import asyncio
import functools
import concurrent
import tagdb
from cmdr import RFIDFrontend
from cmdr import CmdExec
from trusted_cmds import trusted_commands

class SysSigHandler:
    def __init__(self, rfid_frontend):
        self.rfid_frontend = rfid_frontend
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, functools.partial(self.exit_gracefully))
        loop.add_signal_handler(signal.SIGINT, functools.partial(self.exit_gracefully))
        loop.add_signal_handler(signal.SIGUSR1, functools.partial(self.reload_tagdb))
        loop.add_signal_handler(signal.SIGUSR2, functools.partial(self.leak_next_uid))
        loop.add_signal_handler(signal.SIGCHLD, functools.partial(self.child_exit))
    def exit_gracefully(self):
        logging.debug('cancelling tasks...')
        [task.cancel() for task in asyncio.Task.all_tasks()]
        asyncio.get_event_loop().stop()
    def reload_tagdb(self):
        logging.info('reloading tags...')
        importlib.reload(tagdb)
        self.rfid_frontend.uid_db = tagdb.uids
    def leak_next_uid(self):
        self.rfid_frontend.leak_uid = True
    def child_exit(self):
        logging.debug('child process exit')
        os.waitpid(0, 0)

async def rfid_main():
    cmdexec = CmdExec(trusted_commands)
    rfid_frontend = RFIDFrontend(cmdexec, tagdb.uids)
    sig_handler = SysSigHandler(rfid_frontend)
    await rfid_frontend.start_reader()

def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    tasks = [rfid_main()]
    asyncio.ensure_future(asyncio.gather(*tasks, return_exceptions=True))
    try:
        loop.run_forever()
    finally:
        logging.debug('waiting for all tasks done...')
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True))
        loop.close()

if __name__=='__main__':
    main()
