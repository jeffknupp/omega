"""Brokest client library."""
from __future__ import absolute_import
import logging

import zmq

from message import Message
from config.settings import CONFIG

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def async(f):
    a = AsyncTask(f)
    return a

class Result(object):
    def __init__(self, result):
        self._result = result

    def get(self):
        return self._result

    def set_result(self, result):
        self._result = result

class AsyncTask(object):
    def __init__(self, f):
        self._func = f

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def async(self, *args, **kwargs):
        print 'async'
        return self.queue(args, kwargs)

    def queue(self, *args, **kwargs):
        """Return the result of running the task *runnable* with the given
        arguments."""
        message = Message(
            self._func,
            args,
            kwargs)
        LOGGER.info('Sending [{}] with args[{}] and kwargs[{}] to {}:{}'.format(
            self._func,
            message.args,
            message.kwargs,
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))
        socket = zmq.Context().socket(zmq.REQ)
        socket.connect('tcp://{}:{}'.format(
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))
        socket.send_pyobj(message)
        results = socket.recv_pyobj()
        LOGGER.info('Result is [{}]'.format(results))
        return results

    if __name__ == '__main__':
        context = zmq.Context()

        t = zmq.devices.MonitoredQueue(zmq.ROUTER, zmq.DEALER, zmq.PUB)
        t.bind_in('tcp://{}:{}'.format(
            CONFIG['front-end-host'],
            CONFIG['front-end-port']))
        t.bind_out('tcp://{}:{}'.format(
            CONFIG['back-end-host'],
            CONFIG['back-end-port']))
        t.bind_mon('tcp://{}:{}'.format(
            CONFIG['monitor-host'],
            CONFIG['monitor-port']))
        t.start()
