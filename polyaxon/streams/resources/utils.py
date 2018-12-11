import json

from websockets import ConnectionClosed


def get_error_message(message):
    return json.dumps({'status': 'error', 'log_lines': [message]})


def get_status_message(status):
    return json.dumps({'status': status, 'log_lines': None})


def should_disconnect(ws, ws_manager):
    if ws._connection_lost:  # pylint:disable=protected-access
        ws_manager.remove_sockets({ws, })
        return True
    return not ws_manager.ws


async def notify(consumer, message):
    disconnected_ws = set()
    for _ws in consumer.ws:
        try:
            await _ws.send(message)
        except ConnectionClosed:
            disconnected_ws.add(_ws)
    consumer.remove_sockets(disconnected_ws)


async def notify_ws(ws, message):
    try:
        await ws.send(message)
    except ConnectionClosed:
        pass
