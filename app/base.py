import asyncio
import aioamqp
import aiohttp

from .config import BaseConfig

config = BaseConfig()


class BaseRabbit:

    def __init__(self, host=config.RABBIT_HOST, port=config.RABBIT_PORT, queue=config.QUEUE_NAME):
        self.host = host
        self.port = port
        self.queue = queue
        self.transport = None
        self.protocol = None
        self.channel = None

    async def connect(self):
        try:
            self.transport, self.protocol = await aioamqp.connect(host=self.host, port=self.port)
        except aioamqp.AmqpClosedConnection:
            print("closed connections")
            return

    async def close(self):
        await self.protocol.close()
        self.transport.close()

    async def prepare(self):
        self.channel = await self.protocol.channel()
        await self.channel.queue_declare(self.queue)


class Producer(BaseRabbit):

    async def publish(self, message):
        await self.channel.publish(message, '', self.queue)


class Consumer(BaseRabbit):

    @staticmethod
    async def callback(channel, body, envelope, properties):
        return body

    async def consume(self):
        await self.channel.basic_consume(self.callback, queue_name=self.queue, no_ack=True)
