from pydispatch import dispatcher
import logging
import asyncio
import functools
import importlib

class CmdExec:
    """
    A general executor for commands.
    It listens to the "reload" signal to reload the command loopup table.
    It listens to the signal "got_cmd" to execute the shell command.
    """
    def __init__(self, cmd_module):
        self.cmd_module = cmd_module
        dispatcher.connect(self.reload, signal="reload")
        dispatcher.connect(self.run, signal="got_cmd")

    def run(self, cmd_id):
        asyncio.ensure_future(self._run(cmd_id))

    async def _run(self, cmd_id):
        """Execute the specified command.

        Argument:
        cmd_id -- The key for looking up the trusted command.
        """
        try:
            cmd = self.cmd_module.commands[cmd_id]
            if cmd:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(exec, cmd))
        except asyncio.CancelledError:
            logging.debug(self.cmd_module__name__+' command executor stopped')
            raise
        except KeyError:
            logging.warning('Command not found')

    def reload(self):
        importlib.reload(self.cmd_module)
        logging.info(self.cmd_module.__name__+' command list reloaded')
