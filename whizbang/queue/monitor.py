"""Monitor client for brokest broker."""

import sys
import zmq

class Monitor(object):
    def __init__(self, num_messages=0):
        self._num_messages = num_messages
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect('tcp://127.0.0.1:9090')
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self._terminate = False
        self._seen_messages = 0

    def terminate(self):
        self._terminate = True

    def start(self):
        while not self._terminate:
            if self._num_messages and self._num_messages == self._seen_messages:
                break
            message = self.socket.recv()
    
if __name__ == '__main__':
    m = Monitor()
    m.start()
