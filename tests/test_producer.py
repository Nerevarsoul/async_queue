import asyncio

from app.base import Producer


async def test_prepare():
    producer = Producer()
    producer.connect()
    producer.prepare()

    producer.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_prepare())
    loop.close()