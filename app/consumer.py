import argparse
import asyncio
from aiohttp import ClientSession

from app.base import Consumer
from app.config import BaseConfig
from web.config import WebConfig


async def get(channel, body, envelope, properties):
    async with ClientSession() as session:
        for _ in range(config.RETRY):
            response = await session.get(WebConfig.SERVER_URL)
            if response.status == 200:
                print(body)
                break
            await asyncio.sleep(config.COUNTDOWN)


async def listen():
    while True:
        try:
            await consumer.consume(get)
        except Exception as exc:
            print('esc ', exc)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('workers', metavar='W', type=int, help='a count of workers')
    args = parser.parse_args()
    workers = args.workers
    await consumer.connect()
    await consumer.prepare()
    for _ in range(workers):
        asyncio.ensure_future(listen())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    consumer = Consumer()
    config = BaseConfig()
    asyncio.ensure_future(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(consumer.close())
    loop.close()
