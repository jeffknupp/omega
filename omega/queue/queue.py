"""Brokest client library."""
from __future__ import absolute_import
import logging

import zmq
from omega.queue import serialization

from omega.queue.message import Message
from config.settings import CONFIG

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def async(f):
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    wrapped.delay = delay(f)
    return wrapped

class delay(object):
    def __init__(self, f):
        self._func = f
        self.socket = zmq.Context().socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))

    def __call__(self, *args, **kwargs):
        want_results = kwargs.pop('want_results')
        self.queue(self._func, *args, **kwargs)
        if not want_results:
            self.socket.recv_pyobj()
        else:
            return Result(self.socket.recv_pyobj)

    def queue(self, runnable, *args, **kwargs):
        """Return the result of running the task *runnable* with the given
        arguments."""
        message = Message(
                serialization.dumps(runnable),
                args,
                kwargs)
        LOGGER.info('Sending [{}] with args[{}] and kwargs[{}] to {}:{}'.format(
            runnable,
            message.args,
            message.kwargs,
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))
        self.socket.send_pyobj(message)


class Result(object):
    def __init__(self, runnable):
        self._runnable = runnable

    def get(self):
        return self._runnable()
        
class Broker(object):
    def __init__(self):
        self._device = zmq.devices.MonitoredQueue(zmq.ROUTER, zmq.DEALER, zmq.PUB)
        self._device.bind_in('tcp://{}:{}'.format(
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))
        self._device.bind_out('tcp://{}:{}'.format(
            CONFIG['back-end-host'],
            CONFIG['back-end-port']))
        self._device.bind_mon('tcp://{}:{}'.format(
            CONFIG['monitor-host'],
            CONFIG['monitor-port']))

    def start(self):
        self._device.start()
