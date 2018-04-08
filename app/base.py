import asyncio 
import aioamqp
import aiohttp

from app.config import BaseConfig

config = BaseConfig()


class BaseRabbit:

    def __init__(
            self, host=config.RABBIT['host'], port=config.RABBIT['port'],
            exchange_name=config.RABBIT['exchange_name'], routing_key=config.RABBIT['routing_key']
    ):
        self.host = host
        self.port = port
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.transport = None
        self.protocol = None
        self.channel = None
        self.queue = None

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


class Producer(BaseRabbit):

    async def prepare(self):
        await super().prepare()
        await self.channel.exchange_declare(exchange_name=self.exchange_name, type_name='direct')

    async def publish(self, message):
        await self.channel.basic_publish(message, exchange_name=self.exchange_name, routing_key=self.routing_key)


class Consumer(BaseRabbit):

    async def prepare(self):
        await super().prepare()
        await self.channel.exchange(exchange_name=self.exchange_name, type_name='direct')
        result = await self.channel.queue(queue_name='', durable=False, auto_delete=True)
        self.queue = result['queue']
        await self.channel.queue_bind(
            exchange_name=self.exchange_name, queue_name=self.queue, routing_key=self.routing_key
        )

    async def consume(self, callback):
        await self.channel.basic_consume(callback, queue_name=self.queue, no_ack=True)
