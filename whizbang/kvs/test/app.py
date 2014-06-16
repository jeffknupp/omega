import threading

from whizbang.kvs.server import Server
from whizbang.kvs.client import Client

def main():
    server = Server(9090)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    client = Client(9090)
    client.put('foo', 'bar')
    client.get('foo')
    client.get('baz')
    server.stop()
    server_thread.join()
if __name__ == '__main__':
    main()
