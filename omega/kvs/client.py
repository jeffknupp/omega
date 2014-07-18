import zmq


class Client(object):

    def __init__(self, port):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://localhost:{}'.format(port))

    def get(self, key):
        message = {'command': 'GET', 'value': key}
        self._socket.send_json(message)
        response = self._socket.recv_json()
        return response

    def put(self, key, value):
        message = {'command': 'PUT', 'key': key, 'value': value}
        self._socket.send_json(message)
        response = self._socket.recv_json()
        return response


if __name__ == '__main__':
    c = Client(9090)
    print c.put('foo', 'bar')
    print c.get('foo')
