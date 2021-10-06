"""
    @Author varx
    @Date 06/10/21 15.09
    @Describe 
"""
import sys
import asyncio
import json
from aio_pika import connect, Message, DeliveryMode, ExchangeType


async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    logs_exchange = await channel.declare_exchange(
        "logs", ExchangeType.FANOUT
    )

    data = {
        'id':'varx'
    }

    message_body = json.dumps(data).encode()

    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    # Sending the message
    await logs_exchange.publish(message, routing_key="info")

    print(" [x] Sent %r" % message)

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))