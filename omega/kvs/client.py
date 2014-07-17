import zmq

from omega.kvs.message import CommandMessage

class Client(object):

    def __init__(self, port):
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect('tcp://localhost:{}'.format(port))

    def get(self, key):
        message = CommandMessage('get', key)
        self._socket.send_pyobj(message)
        response = self._socket.recv_pyobj()
        print response.outcome, response.value
        return response

    def put(self, key, value):
        message = CommandMessage('put', (key, value))
        self._socket.send_pyobj(message)
        response = self._socket.recv_pyobj()
        print response.outcome, response.value
        return response
