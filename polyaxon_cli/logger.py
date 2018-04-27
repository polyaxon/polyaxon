# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import sys

logger = logging.getLogger('polyaxon.cli')


def configure_logger(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level, stream=sys.stdout)

    from polyaxon_cli.managers.cli import CliConfigManager

    cli_config = CliConfigManager.get_config()
    if cli_config.log_handler:
        import raven

        raven.Client(
            dsn=cli_config.log_handler.decoded_dns,
            release=cli_config.current_version,
            environment=cli_config.log_handler.environment,
            tags=cli_config.log_handler.tags,
            processors=('raven.processors.SanitizePasswordsProcessor',))
