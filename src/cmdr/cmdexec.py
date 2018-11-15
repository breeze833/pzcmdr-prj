from pydispatch import dispatcher
import logging
logger = logging.getLogger('pzcmdr')
import asyncio
import functools

class CmdExec:
    """
    A general executor for commands.
    It listens to the "reload" signal to reload the command loopup table.
    It listens to the signal "got_cmd" to execute the shell command.
    """
    def __init__(self, commands={}):
        """
        Initialize the command executor.

        Argument:
        commands -- The command name to command code lookup table.
        """
        self.commands = commands
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
            cmd = self.commands[cmd_id]
            if cmd:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(exec, cmd))
        except asyncio.CancelledError:
            logger.debug(' command executor stopped')
            raise
        except KeyError:
            logger.warning('Command not found')
        except:
            logger.warning('Command {cmd_id} execution error'.format(cmd_id=cmd_id))
            logger.debug('Command {cmd_id} execution error'.format(cmd_id=cmd_id), exc_info=True)

    def reload(self, commands):
        """
        Reload the command executor lookup table.

        Argument:
        commands -- The command name to command code lookup table.
        """
        self.commands = commands
        logger.info(' command list reloaded')
