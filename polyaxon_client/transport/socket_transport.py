# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import six
import websocket

from polyaxon_client.logger import logger


class SocketTransportMixin(object):
    """Socket operations transport."""
    def socket(self, url, message_handler, headers=None):
        webs = websocket.WebSocketApp(
            url,
            on_message=lambda ws, message: self._on_message(message_handler, message),
            on_error=self._on_error,
            on_close=self._on_close,
            header=self._get_headers(headers)
        )
        return webs

    def stream(self, url, message_handler, headers=None):
        webs = self.socket(url=url, message_handler=message_handler, headers=headers)
        webs.run_forever(ping_interval=30, ping_timeout=10)

    def _on_message(self, message_handler, message):
        if message_handler and message:
            if not isinstance(message, six.string_types):
                message = message.decode('utf-8')
            message_handler(json.loads(message))

    @staticmethod
    def _on_error(ws, error):
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            logger.info('Quitting... The session will be running in the background.')
        else:
            logger.debug('Termination cause: %s', error)
            logger.debug('Session disconnected.')

    @staticmethod
    def _on_close(ws):
        logger.info('Session ended')
