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


async def listen(consumer):
    while True:
        try:
            await consumer.consume(get)
        except Exception as exc:
            print('esc ', exc)


async def main(consumer):
    await consumer.connect()
    await consumer.prepare()
    asyncio.ensure_future(listen(consumer))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    config = BaseConfig()
    consumers = list()
    parser = argparse.ArgumentParser()
    parser.add_argument('workers', type=int, help='a count of workers')
    args = parser.parse_args()
    for _ in range(args.workers):
        worker = Consumer()
        consumers.append(worker)
        asyncio.ensure_future(main(worker))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for worker in consumers:
            loop.run_until_complete(worker.close())
    loop.close()
