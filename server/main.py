import asyncio

PUBLISHER_SERVER_HOST = '127.0.0.1'
PUBLISHER_SERVER_PORT = 9999

SUBSCRIBER_SERVER_HOST = '127.0.0.1'
SUBSCRIBER_SERVER_PORT = 8888

async def handle_publisher(reader, writer):
    # Implementar aqui el manejo de sockets de publishers
    pass


async def handle_subscriber(reader, writer):
    # Implementar aqui el manejo de sockets de subscriptores
    pass


def start_server():
    loop = asyncio.get_event_loop()
    publisher_server_fut = asyncio.start_server(
        handle_publisher, PUBLISHER_SERVER_HOST, PUBLISHER_SERVER_PORT, loop=loop
    )
    subscriber_server_fut = asyncio.start_server(
        handle_subscriber, SUBSCRIBER_SERVER_HOST, SUBSCRIBER_SERVER_PORT, loop=loop
    )
    subscriber_server = loop.run_until_complete(subscriber_server_fut)
    publisher_server = loop.run_until_complete(publisher_server_fut)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        subscriber_server.close()
        publisher_server.close()
        loop.run_until_complete(subscriber_server.wait_closed())
        loop.run_until_complete(publisher_server.wait_closed())
        loop.close()


if __name__ == '__main__':
    start_server()
