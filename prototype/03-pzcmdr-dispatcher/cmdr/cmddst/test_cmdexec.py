from . import test_cmds
from .cmdexec import CmdExec

class TestCmdExec(CmdExec):
    def __init__(self):
        CmdExec.__init__(self, test_cmds)

