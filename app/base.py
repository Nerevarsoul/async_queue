import random
 
import aioamqp

from app.config import BaseConfig

config = BaseConfig()


class BaseRabbit:

    def __init__(
            self, host=config.RABBIT['host'], port=config.RABBIT['port'], exchange_name=config.RABBIT['exchange_name']
    ):
        self.host = host
        self.port = port
        self.exchange_name = exchange_name
        self.transport = None
        self.protocol = None
        self.channel = None
        self.queue = None
        self.severities = []

    async def connect(self):
        try:
            self.transport, self.protocol = await aioamqp.connect(host=self.host, port=self.port)
        except aioamqp.AmqpClosedConnection:
            print("closed connections")
            return

    async def close(self):
        await self.protocol.close()
        self.transport.close()

    async def prepare(self, *args, **kwargs):
        self.channel = await self.protocol.channel()


class Producer(BaseRabbit):

    async def prepare(self, *args, **kwargs):
        await super().prepare()
        await self.channel.exchange_declare(exchange_name=self.exchange_name, type_name='direct', durable=True)

    async def publish(self, message):
        routing_key = str(random.randint(0, config.KEY_RANGE))
        await self.channel.basic_publish(message, exchange_name=self.exchange_name, routing_key=routing_key)


class Consumer(BaseRabbit):

    async def prepare(self, workers, number, *args, **kwargs):
        await super().prepare()
        await self.channel.exchange(exchange_name=self.exchange_name, type_name='direct')
        result = await self.channel.queue(queue_name='', durable=True, auto_delete=True)
        self.queue = result['queue']
        self.severities = [str(i) for i in range(config.KEY_RANGE) if i % workers == number]
        for severity in self.severities:
            await self.channel.queue_bind(
                exchange_name=self.exchange_name, queue_name=self.queue, routing_key=severity
            )

    async def consume(self, callback):
        await self.channel.basic_consume(callback, queue_name=self.queue)
