# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import asyncio
from sanic import Sanic
from sanic.response import text

from websockets import ConnectionClosed

from events.consumers import Consumer

app = Sanic(__name__)


@app.route('/')
async def index(request):
    return text('Hello world!')


@app.websocket('/stream/namespace')
async def namespace(request, ws):
    if request.app.namespace_consumer is None:
        request.app.namespace_consumer = Consumer(
            routing_key=os.environ['POLYAXON_EVENTS_NAMESPACE_ROUTING_KEY'], queue='namespace')
        request.app.namespace_consumer.run()

    request.app.namespace_consumer.add_socket(ws)
    while True:
        for message in request.app.namespace_consumer.get_messages():
            disconnected_ws = set()
            for ws in request.app.namespace_consumer.ws:
                try:
                    await ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(ws)
            request.app.namespace_consumer.remove_sockets(disconnected_ws)
        await asyncio.sleep(1)


@app.websocket('/stream/resources')
async def resources(request, ws):
    if request.app.resources_consumer is None:
        request.app.resources_consumer = Consumer(
            routing_key=os.environ['POLYAXON_EVENTS_RESOURCES_ROUTING_KEY'], queue='namespace')
        request.app.resources_consumer.run()

    request.app.resources_consumer.add_socket(ws)
    while True:
        messages = request.app.resources_consumer.get_messages()
        if messages:
            disconnected_ws = set()
            for ws in request.app.resources_consumer.ws:
                try:
                    await ws.send(messages[-1])
                except ConnectionClosed:
                    disconnected_ws.add(ws)
            request.app.resources_consumer.remove_sockets(disconnected_ws)
        await asyncio.sleep(1)


@app.websocket('/stream/logs')
async def logs(request, ws):
    if request.app.logs_consumer is None:
        request.app.logs_consumer = Consumer(
            routing_key=os.environ['POLYAXON_JOB_RESOURCES_ROUTING_KEY'], queue='namespace')
        request.app.logs_consumer.run()

    request.app.logs_consumer.add_socket(ws)
    while True:
        for message in request.app.logs_consumer.get_messages():
            disconnected_ws = set()
            for ws in request.app.logs_consumer.ws:
                try:
                    await ws.send(message)
                except ConnectionClosed:
                    disconnected_ws.add(ws)
            request.app.logs_consumer.remove_sockets(disconnected_ws)
        await asyncio.sleep(1)


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    app.namespace_consumer = None
    app.resources_consumer = None
    app.logs_consumer = None


@app.listener('after_server_stop')
async def notifiy_server_stoped(app, loop):
    if app.namespace_consumer:
        app.namespace_consumer.stop()
    if app.resources_consumer:
        app.resources_consumer.stop()
    if app.logs_consumer:
        app.logs_consumer.stop()
