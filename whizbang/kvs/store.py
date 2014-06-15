import zmq

class KVStore(object):
    def __init__(self):
        self._store = {}

    def put(self, key, value):
        self._store[key] = value

    def get(self, key):
        return self._store.get(key, None)

class Server(object):
    def __init__(self, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind('tcp://*:{}'.format(port))

    def start(self):
        while True:
            message = self.socket.recv_json()
            

s = Server(9000)
s.start()
