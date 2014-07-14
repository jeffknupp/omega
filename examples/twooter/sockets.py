from socketio.namespace import BaseNamespace


class ChatNamespace(BaseNamespace):
    sockets = {}

    def on_chat(self, msg):
        self.emit('chat', msg)

    def recv_connect(self):
        print "Got a socket connection"
        self.sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        print "Got a socket disconnection"
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    @classmethod
    def broadcast(self, event, message):
        for ws in self.sockets.values():
            ws.emit(event, message)
