import asyncio

PUBLISHER_SERVER_HOST = '127.0.0.1'
PUBLISHER_SERVER_PORT = 9999

SUBSCRIBER_SERVER_HOST = '127.0.0.1'
SUBSCRIBER_SERVER_PORT = 8888

#publishers = []
subscribers = []

async def handle_publisher(reader, my_writer):
    # Implementar aqui el manejo de sockets de publishers
    #publishers.append(reader)
    try :
        while True :
            message_length_bytes = await reader.read(4)
            message_length = int.from_bytes(
            message_length_bytes, byteorder='big')
            message = await reader.read(message_length)
            for subscriber in subscribers:
                #if subscriber != my_writer:
                subscriber.write(message_length_bytes)
                subscriber.write(message)
    except IncompleteReadError:
        pass
        #publishers.remove(my_writer)


async def handle_subscriber(reader, my_writer):
    # Implementar aqui el manejo de sockets de suscriptores
    subscribers.append(my_writer)
    try :
        while True :
            for subscriber in subscribers:
                #if subscriber != reader:
                    #asyncio.Protocol.data_received(data)
                message_length_bytes = await reader.read(4)
                message_length = int.from_bytes(
                message_length_bytes, byteorder='big')
                message = await reader.read(message_length)
    except IncompleteReadError:
       subscribers.remove(my_writer)


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

    # Serve requests until Ctrl+C is pressed
    print('Serving subscribers on {}'.format(subscriber_server.sockets[0].getsockname()))
    print('Serving publishers on {}'.format(publisher_server.sockets[0].getsockname()))

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
