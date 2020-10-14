#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import logging
import sys

from functools import wraps

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


logger = logging.getLogger("polyaxon.cli")


def configure_logger(verbose):
    # DO NOT MOVE OUTSIDE OF THE FUNCTION!
    from polyaxon import settings
    from polyaxon.plugins.sentry import set_raven_client

    if verbose or settings.CLIENT_CONFIG.debug:
        log_level = logging.DEBUG
        settings.CLIENT_CONFIG.debug = True
    else:
        if not settings.CLIENT_CONFIG.disable_errors_reporting:
            set_raven_client()
        log_level = logging.INFO
        if settings.CLIENT_CONFIG.log_level:
            try:
                log_level = logging.getLevelName(settings.CLIENT_CONFIG.log_level)
            except:  # noqa
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
