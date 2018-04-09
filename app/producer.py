import asyncio

from app.base import Producer, config


async def main():
    await producer.connect()
    await producer.prepare()
    while True:
        await producer.publish('Some text')
        await asyncio.sleep(config.PERIOD)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    producer = Producer()
    asyncio.ensure_future(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(producer.close())
    loop.close()
