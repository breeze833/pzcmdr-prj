from pydispatch import dispatcher
import logging
import importlib
from . import tagdb

class UID2Cmd:
    """
    Lookup the command by the given UID.
    It listens to the signal "got_uid" and send the command with the signal "got_cmd".
    It also listens to the signal "reload" to reload the UID lookup table.
    """
    def __init__(self):
        """
        Initialize the lookup component.
        """
        dispatcher.connect(self.find_cmd, signal="got_uid")
        dispatcher.connect(self.reload, signal="reload")

    def find_cmd(self, uid):
        cmd = None
        try:
            cmd = tagdb.uids[uid][0]
            dispatcher.send("got_cmd", self, cmd)
        except KeyError:
            logging.warning('UID not found')
            dispatcher.send("got_error", self, uid)

    def reload(self):
        importlib.reload(tagdb)
        logging.info('UID lookup table reloaded')
