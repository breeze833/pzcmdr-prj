from pydispatch import dispatcher
import logging
logger = logging.getLogger('pzcmdr')

class UID2Cmd:
    """
    Lookup the command by the given UID.
    It listens to the signal "got_uid" and send the command with the signal "got_cmd".
    It also listens to the signal "reload" to reload the UID lookup table.
    """
    def __init__(self, uids={}):
        """
        Initialize the lookup component.

        Argument:
        uids -- The lookup table from UID to command
        """
        self.uids = uids
        dispatcher.connect(self.find_cmd, signal="got_uid")
        dispatcher.connect(self.reload, signal="reload")

    def find_cmd(self, uid):
        cmd = None
        try:
            cmd = self.uids[uid][0]
            dispatcher.send("got_cmd", self, cmd)
        except KeyError:
            logger.warning('UID not found')
            dispatcher.send("got_error", self, uid)

    def reload(self, uids):
        """
        Reload the lookup table.

        Arguments:
        uids -- The lookup table from UID to command.
        """
        self.uids = uids
        logger.info('UID lookup table reloaded')
