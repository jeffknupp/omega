import zmq
from omega.kvs.message import CommandMessage, StatusMessage

class KVStore(object):
    def __init__(self):
        self._store = {}

    def put(self, key, value):
        self._store[key] = value

    def get(self, key):
        return self._store.get(key, None)

    def delete(self, key):
        del self._store[key]

class Server(object):
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind('tcp://*:{}'.format(port))
        self._store = KVStore()
        self._terminate = False

    def stop(self):
        self._terminate = True

    def start(self):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)
        while not self._terminate:
            events = poll.poll(1000)
            if events:
                message = self.socket.recv_pyobj()
                if message.command == 'get':
                    self.socket.send_pyobj(StatusMessage('OK', self._store.get(message.value)))
                elif message.command == 'put':
                    key, value = message.value
                    self._store.put(key, value)
                    self.socket.send_pyobj(StatusMessage('OK'))
