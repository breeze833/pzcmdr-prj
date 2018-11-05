import logging

class CmdExec:
    def __init__(self, trusted_cmds={}):
        """Initialize a command executor.

        Argument:
        trusted_cmds -- a dictionary that contains the supported commands.
        """
        self.trusted_cmds = trusted_cmds

    def run(self, cmd_id):
        """Execute the specified command.

        Argument:
        cmd_id -- The key for looking up the trusted command.
        """
        try:
            cmd = self.trusted_cmds[cmd_id]
            if cmd:
                exec(cmd)
        except KeyError:
            logging.warning('Command not found')

