import pytest
import asyncio

from multiprocessing import Process

import time

from server.main import start_server

PUBLISHER_SERVER_HOST = '127.0.0.1'
PUBLISHER_SERVER_PORT = 9999

SUBSCRIBER_SERVER_HOST = '127.0.0.1'
SUBSCRIBER_SERVER_PORT = 8888


class Client:
    def __init__(self, ip, port, loop):
        self.loop = loop
        self.reader, self.writer = None, None
        self.ip = ip
        self.port = port

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.ip, self.port, loop=self.loop)

    async def send_data(self, data: bytes):
        data_len = len(data)
        data_len_in_bytes = data_len.to_bytes(4, byteorder='big')
        self.writer.write(data_len_in_bytes)
        self.writer.write(data)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await self.read_data()
        except asyncio.IncompleteReadError:
            raise StopAsyncIteration

    def read_data_iter(self):
        return self

    async def read_data(self):
        data_len_in_bytes = await self.reader.read(4)
        data_len = int.from_bytes(data_len_in_bytes, byteorder='big')
        data = await self.reader.read(data_len)
        return data

    def close(self):
        self.writer.close()


@pytest.fixture
def server():
    process = Process(target=start_server)
    process.start()
    time.sleep(1)
    yield process
    process.terminate()


@pytest.fixture
def subscriber_client(event_loop, server):
    subscriber_client = Client(SUBSCRIBER_SERVER_HOST, SUBSCRIBER_SERVER_PORT, event_loop)
    event_loop.run_until_complete(subscriber_client.connect())
    yield subscriber_client
    subscriber_client.close()


@pytest.fixture
def publisher_client(event_loop, server):
    publisher_client = Client(PUBLISHER_SERVER_HOST, PUBLISHER_SERVER_PORT, event_loop)
    event_loop.run_until_complete(publisher_client.connect())
    yield publisher_client
    publisher_client.close()


@pytest.mark.asyncio
async def test_open_connection_to_subscriber_server(event_loop, server):
    subscriber_client = Client(SUBSCRIBER_SERVER_HOST, SUBSCRIBER_SERVER_PORT, event_loop)
    await subscriber_client.connect()


@pytest.mark.asyncio
async def test_open_connection_to_publisher_server(event_loop, server):
    publisher_client = Client(PUBLISHER_SERVER_HOST, PUBLISHER_SERVER_PORT, event_loop)
    await publisher_client.connect()


@pytest.mark.asyncio
async def test_publish_one_message(publisher_client, subscriber_client):
    message = b"testing"
    await publisher_client.send_data(message)
    received_message = await subscriber_client.read_data()
    assert message == received_message


@pytest.mark.asyncio
async def test_publish_one_message_to_ten_subscribers(publisher_client, event_loop):
    number_of_subscribers = 10
    subscribers_clients = [
        Client(SUBSCRIBER_SERVER_HOST, SUBSCRIBER_SERVER_PORT, event_loop) for _ in range(number_of_subscribers)
        ]

    for subscriber_client in subscribers_clients:
        await subscriber_client.connect()

    message = b'testing'
    await publisher_client.send_data(message)

    for subscriber_client in subscribers_clients:
        received_message = await subscriber_client.read_data()
        assert received_message == message


@pytest.mark.asyncio
async def test_publish_ten_message_to_one_subscribers(subscriber_client, event_loop):
    number_of_publishers = 10
    publishers_clients = [
        Client(PUBLISHER_SERVER_HOST, PUBLISHER_SERVER_PORT, event_loop) for _ in range(number_of_publishers)
        ]

    message = b'testing'

    for publisher_client in publishers_clients:
        await publisher_client.connect()
        await publisher_client.send_data(message)

    for _ in range(number_of_publishers):
        data = await subscriber_client.read_data()
        assert data == message
