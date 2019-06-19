# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_cli.managers.auth import AuthConfigManager
from polyaxon_cli.managers.config import GlobalConfigManager
from polyaxon_cli.utils.formatting import Printer
from polyaxon_client import PolyaxonClient as BasePolyaxonClient


class PolyaxonClient(BasePolyaxonClient):
    def __init__(self):
        host = GlobalConfigManager.get_value('host')
        if not host:
            Printer.print_error('Received an invalid config, you need to provide a valid host.')
            sys.exit(1)
        port = GlobalConfigManager.get_value('port')
        use_https = GlobalConfigManager.get_value('use_https')
        verify_ssl = GlobalConfigManager.get_value('verify_ssl')
        token = AuthConfigManager.get_value('token')
        super(PolyaxonClient, self).__init__(
            host=host,
            http_port=port,
            ws_port=port,
            use_https=use_https,
            verify_ssl=verify_ssl,
            token=token,
            schema_response=True,
            reraise=True,
        )
