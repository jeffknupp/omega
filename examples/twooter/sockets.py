"""SocketIO implementation for Chatting. Requires very small amount of code."""

from socketio.namespace import BaseNamespace


class ChatNamespace(BaseNamespace):
    """A namespace to handle chatting."""
    sockets = {}

    def on_chat(self, msg):
        """Act on a *chat* event."""
        ChatNamespace.emit('chat', msg)

    def recv_connect(self):
        """Add the connected socket to the given socket."""
        print "Got a socket connection"
        self.sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        """Remove the given socket from the list."""
        print "Got a socket disconnection"
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    @classmethod
    def broadcast(cls, event, message):
        """Broadcast the message to all connected sockets."""
        for write_socket in cls.sockets.values():
            write_socket.emit(event, message)
