import json

from websockets import ConnectionClosed


def get_error_message(message):
    return json.dumps({'status': 'error', 'log_lines': [message]})


def get_status_message(status):
    return json.dumps({'status': status, 'log_lines': None})


async def notify(consumer, message):
    disconnected_ws = set()
    for _ws in consumer.ws:
        try:
            await _ws.send(message)
        except ConnectionClosed:
            disconnected_ws.add(_ws)
    consumer.remove_sockets(disconnected_ws)
