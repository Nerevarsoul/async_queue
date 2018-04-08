from aiohttp import web

from .config import WebConfig

config = WebConfig()


async def handler(request):
    data = await request.json()
    print(data)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', handler)
    web.run_app(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
