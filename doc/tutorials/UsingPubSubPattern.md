Using Publisher-Subscriber Pattern
==================================

The asynchronous behavior is largely depends on the I/O operations.
A co-routine may be temporarily suspended after issuing and I/O request.
It continues execution later when the I/O operation is completed.
We may imagine that the system sends events representing various kinds of I/O conditions to the event loop.
The event loop processes an event and schedule the proper co-routine for execution.
This is a typical event-driven pardigm.
The system is the event provider, the co-routine is the event consumer, and the event loop is the intermediate event-dispatching mechanism.
This matches the *publisher-subscriber* (pubsub) design pattern.

We examined the code of the prototype and discovered that some of the component types were hard-coded as object references.
It was a sign of degraded extensibility and flexibility.
Since we expected that some other types of components would be integrated into the application,
it was better to decouple the type-dependent inter-relationships.
One of the approaches is the publisher-subscriber pattern (how coincident!).

Reading a few commnets, we decided to use the popular **PyDispatcher** in our application.

PyDispatcher
------------

Installing PyDispatcher is straightforward:

    pip3 install PyDispatcher

Then, import the dispather from the module:

    from pydispatch import dispatcher

The API is simple and we only need two of the functions.

* `dispatcher.connect(callback, signal='signal_name')`
* `dispatcher.send(signal='signal_name', sender=..., data...)`

The former one is used to associate the callback function when the given signal occurs.
The signal is software-defined. Therefore, we need to define the signal names for our application.
The latter is used to send the signal. The sender is also required and its default value is `dispatcher.Any`.
The data parameters are optional. If they are specified, they will be passed to the call back functions as parameters.


Decoupling the Component Type Dependency
----------------------------------------

To use the dispatcher, we need to define the signal names:

* `start_rfid_reader` / `stop_rfid_reader` trigger the reader-controlling functions.
* `got_uid` indicates that a tag is sensed and the UID is sent as the data parameter.
* `got_cmd` indicates that a command is determined by the UID and the command name is sent as the data parameter.
* `reload` triggers the configuration-reloading.
* `toggle_leak_uid` toggles the logging of the UIDs to a owner-only file.

After revising the components, their dependencies are indirect via the dispatcher.
The type-dependencies are eliminated because all the function invocations are represented by signal names and data parameters.


Summary
-------

In this prototype, we learn how to use the PyDispatcher module to provide the publisher-subscriber pattern for software-defined events.
The communications among processing components are indirect via the dispatcher.
This approach introduces overhead but greatly increase the extensibility and flexibility of the application.

