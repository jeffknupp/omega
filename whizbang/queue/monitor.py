"""Monitor client for brokest broker."""

import sys
import zmq

def main():
    socket = zmq.Context().socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:9090')
    socket.setsockopt(zmq.SUBSCRIBE, '')
    while True:
        message = socket.recv()
        print message
    
if __name__ == '__main__':
    sys.exit(main())
