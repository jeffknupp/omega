"""Broker-less distributed task queue."""
from __future__ import absolute_import
import pickle
import logging
import multiprocessing

import zmq

from config.settings import CONFIG

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Worker(object):
    """A remote task executor."""

    def __init__(self, host='127.0.0.1', port=7080, worker_id=0):
        """Initialize worker."""
        LOGGER.info('Starting worker [{}]'.format(worker_id))
        self.host = host
        self.port = port
        self._id = worker_id
        self._context = None
        self._socket = None

    def start(self):
        """Start listening for tasks."""
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.connect('tcp://{}:{}'.format(
            CONFIG['back-end-host'],
            CONFIG['back-end-port']))
        while True:
            message = self._socket.recv_pyobj()
            runnable = pickle.loads(message.runnable_string)
            args = message.args
            kwargs = message.kwargs
            response = self._do_work(runnable, args, kwargs)
            self._socket.send_pyobj(response)

    def _do_work(self, task, args, kwargs):
        """Return the result of executing the given task."""
        LOGGER.info('[{}] running [{}] with args [{}] and kwargs [{}]'.format(self._id,
            task, args, kwargs))
        return task(*args, **kwargs)

if __name__ == '__main__':
    w = Worker()
    w.start()
