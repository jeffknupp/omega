"""Tests for the KVStore."""


import threading

import pytest

from omega.kvs.server import KVStore, Server
from omega.kvs.client import Client
from omega.kvs.message import CommandMessage, StatusMessage

@pytest.yield_fixture
def server():
    server = Server(9090)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    yield
    server.stop()
    server_thread.join()

@pytest.fixture
def client():
    client = Client(9090)
    return client

def test_set_from_client(server, client):
    response = client.put('foo', 'bar') 
    assert response == StatusMessage('OK')
