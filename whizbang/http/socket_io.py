from socketio.namespace import BaseNamespace

class ChatNamespace(BaseNamespace):
    def on_chat(self, msg):
        self.emit('chat', msg)

class ShoutsNamespace(BaseNamespace):
    sockets = {}
    def recv_connect(self):
        print "Got a socket connection" # debug
        self.sockets[id(self)] = self
    def disconnect(self, *args, **kwargs):
        print "Got a socket disconnection" # debug
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(ShoutsNamespace, self).disconnect(*args, **kwargs)
    # broadcast to all sockets on this channel!
    @classmethod
    def broadcast(self, event, message):
        for ws in self.sockets.values():
            ws.emit(event, message)
