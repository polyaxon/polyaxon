# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import websocket

from polyaxon_client.logger import logger


class SocketTransportMixin(object):
    """Socket operations transport."""
    def socket(self, url, message_handler, headers=None):
        wes = websocket.WebSocketApp(
            url,
            on_message=lambda ws, message: self._on_message(message_handler, message),
            on_error=self._on_error,
            on_close=self._on_close,
            header=self._get_headers(headers)
        )
        wes.run_forever(ping_interval=30, ping_timeout=10)

    def _on_message(self, message_handler, message):
        message_handler(json.loads(message))

    def _on_error(self, ws, error):
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            logger.info('Quitting... The session will be running in the background.')
        else:
            logger.debug('Termination cause: %s', error)
            logger.debug('Session disconnected.')

    def _on_close(self, ws):
        logger.info('Session ended')
