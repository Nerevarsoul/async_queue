import asyncio

from app.base import Consumer


async def test_prepare():
    consumer = Consumer()
    consumer.connect()
    consumer.prepare(5, 1)
    assert consumer.queue is not None
    assert len(consumer.severities) == 12
    assert '1' in consumer.severities
    consumer.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_prepare())
    loop.close()
