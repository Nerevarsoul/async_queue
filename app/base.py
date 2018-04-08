import asyncio 
import aioamqp
import aiohttp

from app.config import BaseConfig

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


class Producer(BaseRabbit):

    async def prepare(self):
        await super().prepare()
        await self.channel.exchange_declare(exchange_name='logs', type_name='direct')    

    async def publish(self, message):
        await self.channel.basic_publish(message, exchange_name='logs', routing_key='info')


class Consumer(BaseRabbit):

    async def prepare(self):
        await super().prepare()
        await self.channel.exchange(exchange_name='logs', type_name='direct')
        result = await self.channel.queue(queue_name='', durable=False, auto_delete=True)
        self.queue = result['queue']
        await self.channel.queue_bind(exchange_name='logs', queue_name=self.queue, routing_key='info')

    async def consume(self, callback):
        await self.channel.basic_consume(callback, queue_name=self.queue, no_ack=True)

