import asyncio

from app.base import Producer


async def main():
    await producer.connect()
    await producer.prepare()
    while True:
        await producer.publish('I love Kate!')
        print('done')
        await asyncio.sleep(1)


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
