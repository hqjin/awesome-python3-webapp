#!/usr/bin/env python
import logging;logging.basicConfig(level=logging.INFO)
from aiohttp import web
import asyncio,os,json,time
from datetime import datetime
def index(request):
    return web.Response(body=b'<!DOCTYPE html><html><h1>Awesome</h1></html>',content_type='text/html' )
@asyncio.coroutine
def init(loop):
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)#对首页/进行响应
    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)#Web App将在9000端口监听HTTP请求
    logging.info('server started at http://127.0.0.1:9000...')
    return srv
loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

