from . import trusted_cmds
from .cmdexec import CmdExec

class TrustedCmdExec(CmdExec):
    def __init__(self):
        CmdExec.__init__(self, trusted_cmds)

