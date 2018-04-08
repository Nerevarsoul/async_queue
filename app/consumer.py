import asyncio
from aiohttp import ClientSession

from app.base import Consumer
from web.config import WebConfig


async def get(channel, body, envelope, properties):
    async with ClientSession() as session:
        for i in range(5):
            response = await session.get(WebConfig.SERVER_URL)
            if response.status == 200:
                print(body)
                break
            await asyncio.sleep(5)


async def listen(consumer, session):
    while True:
        try:
            await consumer.consume(get)
        except Exception as exc:
            print('esc ', exc)

async def main():
    await consumer.connect()
    await consumer.prepare()
    async with ClientSession() as session:
        asyncio.ensure_future(listen(consumer, session))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    consumer = Consumer()
    asyncio.ensure_future(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(consumer.close())
    loop.close()
