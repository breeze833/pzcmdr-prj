import logging
import asyncio
import signal
from pydispatch import dispatcher
from cmdr import VC0706

def shutdown():
    logging.debug('cancelling all tasks...')
    [task.cancel() for task in asyncio.Task.all_tasks()]
    asyncio.get_event_loop().stop()

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    cam = VC0706()

    loop.add_signal_handler(signal.SIGINT, shutdown)

    dispatcher.send('start_capture')

    try:
        loop.run_forever()
    finally:
        logging.debug('waiting for all tasks done...')
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks(), return_exceptions=True))
        loop.close()

