import zmq

class Client(object):

    def __init__(self, port):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://localhost:{}'.format(port))

    def get(self, key):
        message = {'command': 'get', 'key': key}
        self._socket.send_json(message)
        value = self._socket.recv_json()
        print value
        return value

    def put(self, key, value):
        message = {'command': 'put', 'key': key, 'value': value}
        self._socket.send_json(message)
        response = self._socket.recv_json()
        print response
        return response

c = Client(9000)
c.put('foo', 'bar')
c.get('foo')
