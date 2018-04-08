from aiohttp import web

from web.config import WebConfig

config = WebConfig()


async def handler(request):
    print('s!')
    return web.Response()


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', handler)
    web.run_app(app, host=config.SERVER_HOST, port=config.SERVER_PORT)
