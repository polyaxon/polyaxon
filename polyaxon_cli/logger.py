# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import sys

from functools import wraps

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


logger = logging.getLogger('polyaxon.cli')


def configure_logger(verbose):
    def set_raven_client():
        from polyaxon_cli.managers.cli import CliConfigManager

        cli_config = CliConfigManager.get_config()
        if cli_config and cli_config.log_handler and cli_config.log_handler.decoded_dns:
            import raven

            return raven.Client(
                dsn=cli_config.log_handler.decoded_dns,
                release=cli_config.current_version,
                environment=cli_config.log_handler.environment,
                tags=cli_config.log_handler.tags,
                processors=('raven.processors.SanitizePasswordsProcessor',))
        return None

    set_raven_client()
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(message)s', level=log_level, stream=sys.stdout)


def clean_outputs(fn):
    """Decorator for CLI with Sentry client handling.

    see https://github.com/getsentry/raven-python/issues/904 for more details.
    """

    @wraps(fn)
    def clean_outputs_wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except SystemExit as e:
            sys.stdout = StringIO()
            sys.exit(e.code)  # make sure we still exit with the proper code
        except Exception as e:
            sys.stdout = StringIO()
            raise e

    return clean_outputs_wrapper
