#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

def index(request) :
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')
    
# @asyncio.coroutine    # 3.5 以前
async def init(loop) :
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    # srv = yield from loop.create_server(app.make_handler(), '', 80)   # 3.5 以前
    srv = await loop.create_server(app.make_handler(), '', 80)
    logging.info('server started...')
    return srv
    
loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()