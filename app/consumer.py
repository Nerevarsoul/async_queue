import argparse
import asyncio
import logging
from aiohttp import ClientSession

from app.base import Consumer, config
from web.config import WebConfig


async def get(channel, body, envelope, properties):
    async with ClientSession() as session:
        for _ in range(config.RETRY):
            response = await session.get(WebConfig.SERVER_URL)
            if response.status == 200:
                logging.info(body)
                await channel.basic_client_ack(envelope.delivery_tag)
                break
            await asyncio.sleep(config.COUNTDOWN)


async def listen(consumer):
    while True:
        await consumer.consume(get)


async def main(consumer, workers, number):
    await consumer.connect()
    await consumer.prepare(workers, number)
    asyncio.ensure_future(listen(consumer))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    logging.basicConfig(filename=config.LOG['filename'], level=config.LOG['level'])
    consumers = list()
    parser = argparse.ArgumentParser()
    parser.add_argument('workers', type=int, help='a count of workers')
    args = parser.parse_args()
    for number in range(args.workers):
        worker = Consumer()
        consumers.append(worker)
        asyncio.ensure_future(main(worker, args.workers, number))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for worker in consumers:
            loop.run_until_complete(worker.close())
    loop.close()
