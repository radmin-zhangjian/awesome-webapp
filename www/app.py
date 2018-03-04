#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import logging; logging.basicConfig(level=logging.INFO)

import orm, asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request) :
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')
    
async def on_close(app):
    await orm.close_pool()
    
# @asyncio.coroutine    # 3.5 以前
async def init(loop) :
    app = web.Application(loop=loop)
    app.on_shutdown.append(on_close)
    app.router.add_route('GET', '/', index)
    # srv = yield from loop.create_server(app.make_handler(), '', 80)   # 3.5 以前
    # srv = await loop.create_server(app.make_handler(), '', 9000)
    handler = app.make_handler()
    srv = await loop.create_server(handler, '127.0.0.1', 9000)
    logging.info('server started...')
    # return srv
    
    rs = dict()
    rs['app'] = app
    rs['srv'] = srv
    rs['handler'] = handler
    return rs
    
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init(loop))
# loop.run_forever()

loop = asyncio.get_event_loop()
rs = loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    rs['srv'].close()
    loop.run_until_complete(rs['srv'].wait_closed())
    loop.run_until_complete(rs['app'].shutdown())
    loop.run_until_complete(rs['handler'].finish_connections(60.0))
    loop.run_until_complete(rs['app'].cleanup())
loop.close()