Making It Asynchronous
======================

The first prototype is implemented in the conventional *synchronous* approach.
In other words, a function call should finish the task before it returns to the caller.
Regarding to the I/O operations, the typical configuration is to work in *blocking* mode.
For example, the socket reading operation would suspend the thread if there is no data in the input buffer.
To avoid blocking the thread forever, we may configure it to *non-blocking* mode.
In this mode, the reading operation returns with an error when no data is avaiable.
Therefore, working in non-blocking mode usually implies a polling based algorithm.
Polling may consume an amount of CPU cycles and thus be considered inefficient.
A alternative approach is to use the `select()` system call.
The CPU monitors the given file descriptors and allow us to process whenever data is available on a file descriptor.
This approach multiplexes the tasks for multiple descriptors.
The result is a multiplexing or *asynchronous* approach of the program flow.

From Python 3.4 and up, the high-level asynchronous mechanism is builtin as the `asyncio` module.
We would like to design our application to be asynchronous:

* The project will include more concurrent snesing tasks.
  Comparing to multi-thread implementation, asynchronous approach consumes less resources.
  This is proper for Pi Zero.
* We would like to practice with the `asyncio` API.


Using `asyncio`
---------------

The `asyncio` provides the utilies to execute asynchronous tasks.
The concept of **co-routine** is that the function execution can be multiplexed with the others.
Therefore, when defining a co-routine, we need to define the points where it can yield the execution privilege to the others.
Typically the points are I/O related functions due to waiting for the data.
To specify that a function is a co-routine, we use the `async` keyword. To specify the multiplex point, we use the `await` keyword.

    async def coroutine1():
        v = await coroutine2()

    async def coroutine2():
        await asyncio.sleep(1)
        return 3

Note that calling an async function returns a co-routine object.
The coroutine object is executed when it is `await`ed or scheduled as a task.

A task is a scheduled co-routine. It is executed by the *event loop*.
The `asyncio` module initializes an event loop and we can get the reference by

    loop = asyncio.get_event_loop()

To start the event loop to execute a co-routine (it is implicitly converted to a task):

    loop.run_until_complete(coroutine1())

If we have multiple co-routines to execute, the `gather()` method can be used:

    loop.run_until_complete( asyncio.gather(coroutine1(), coroutine2()) )

We may simply start the event loop forever:

    loop.run_forever()

Later a task can be added by `loop.create_task()` or my preferred one:

    asyncio.ensure_future(coroutine1())


Converting a Blocking Call to Asynchronous
------------------------------------------

If we have a long-running function (either computation intensive or I/O waiting),
to allow asychronous execution. It can be wrapped as a co-routine:

    await asyncio.run_in_executor(None, long_running_func)

If the `long_running_func` requires parameters, we may wrap it by `functools`

    await asyncio.run_in_executor(None, functools.partial(long_running_func, param))

An executor is actually a thread. This approach simply grab a worker from the thread pool, start
the function using the thread, and wait for it complete.


Properly Shutdown the Event Loop
--------------------------------

To gracefully shutdown the event loop invoves a few tricks. First we need to cancel all the running tasks.

    tasks_iter = asyncio.Task.all_tasks()
    [task.cancel() for task in tasks_iter]

Note that `task.cancel()` does not stop the task. It simply arranges a task to be cancelled.
Therefore, we need to keep the event loop running fo a while to complete all the tasks.
The tricky *a while* can be guaranteed by the following approach:

* After all the task.canel() are called, stop the loop by `loop.stop()`.
* In the main procedure, use the `finally` block to restart the loop to clear all the tasks.
* The final step is to close the loop `loop.close()`.

The pattern in the main procedure looks like this:

    # setup the application
    ....
    # schedule the entry task(s)
    asyncio.ensure_future(entry_coroutine())

    # start the event loop
    loop = asyncio.get_event_loop()

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(asyncio.gather( *asyncio.Task.all_tasks(), return_exceptions=True ))
        loop.close()

The `return_exceptions=True` suppress the raised exceptions so that we don't need to handle them in the `finally` block.


CancelledError exception
------------------------

When a task receives the cancel request, the `asyncio.CancelledError` is raised for it.
Within the task, you may catch the exception and perform the cleanup procedure.
After that, don't forget to **re-`raise`** the exception.
Without raising `asyncio.CancelledError` to the outer scope, the event loop cannot determine the finish of the task cancellation.

Cancelling an Executor
----------------------

Unfortunately, there is no way to directly cancel the task wrapped by `run_in_executor()`.
If it is allowed, the task would destroyed at an unexpected run-time state.
Therefore, to allow graceful termination, we need to design kind of termination flag in the running algorithm.
When the algorithm is defined by our project, it is very likely to design the flag.
However, the pi-rc522 `wait_for_tag()` call is waiting for the IRQ. It seems that only the hardware signal can force the operation complete.
In other words, we can only attach an RFID tag to trigger the IRQ for terminating the executor.

By examining the source code carefully, we discovered that the function uses the `threading` `Event` object to block until the IRQ is received.
Thus, we can manually issue the `Event.set()` to cheat the function for leaving the waiting state.
This trick solves the problem of cancelling the RC522 reading thread.


Exit the Program
----------------

In the previous prototype, the `SIGINT` and `SIGTERM` handlers invoke the `exit()`.
We catched the `SystemExit` excpetion and called the cleanup procedure.
This approach caused many problems when shutting down the event loop.
It takes several hours before we understood that `exit()` invokes the handlers resgistered to `atexit`.
One of the handlers is registered by the `asyncio` module to **close()** the loop.
When we caught the `SystemExit` exception, the loop is closed and not available anymore.

The correct way is to cancel the tasks and stop the loop.
Let the main procedure to restart the loop, finish all the tasks, and close the loop.

Summary
-------

In this prototype, no new application-level functions are added.
The application is re-implemented by using the asynchronous functionality provoded by Python 3.5.
We learned and practiced the `asyncio` related techniques.

* event loop
* co-routine
* task
* executor
* cancel a task
* exit handling

