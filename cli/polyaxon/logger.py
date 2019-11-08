#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8
from __future__ import absolute_import, division, print_function

import logging
import sys

from functools import wraps

from polyaxon import settings

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


logger = logging.getLogger("polyaxon.cli")


def configure_logger(verbose):
    def set_raven_client():
        from polyaxon.managers.cli import CliConfigManager

        cli_config = CliConfigManager.get_config()
        if cli_config and cli_config.log_handler and cli_config.log_handler.decoded_dsn:
            import sentry_sdk

            sentry_sdk.init(
                dsn=cli_config.log_handler.decoded_dsn,
                release=cli_config.current_version,
                environment=cli_config.log_handler.environment,
            )

    if verbose:
        log_level = logging.DEBUG
        settings.CLIENT_CONFIG.debug = True
    else:
        set_raven_client()
        log_level = logging.INFO
    logging.basicConfig(format="%(message)s", level=log_level, stream=sys.stdout)


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
