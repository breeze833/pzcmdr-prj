from pydispatch import dispatcher
import logging
logger = logging.getLogger('pzcmdr')
import os

class UIDLogger:
    """
    Write the UID to the given file.
    It listens to the signal "toggle_leak_uid" to alter the flag.
    It listens to the signal "got_uid" to obtain the UID and write to file if necessary.
    """
    def __init__(self, filename='leak_uid.txt'):
        """
        Initialize the writer.

        Argument:
        filename -- The output file name.
        """
        self.filename = filename
        self.need_leak_uid = False
        dispatcher.connect(self.toggle_need_leak, signal="toggle_leak_uid")
        dispatcher.connect(self.leak_uid, signal="got_uid")

    def leak_uid(self, uid):
        if self.need_leak_uid:
            fd = os.open('leak_uid.txt', os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'w') as f:
                f.write(str(uid))

    def toggle_need_leak(self):
        self.need_leak_uid = not self.need_leak_uid
        logger.debug('Leak UID: '+str(self.need_leak_uid))

