#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
import functools

from polyaxon_sdk.rest import ApiException
from urllib3.exceptions import HTTPError

from polyaxon import settings
from polyaxon.logger import logger


def client_handler(
    check_no_op: bool = True,
    check_offline: bool = False,
    can_log_events: bool = False,
    can_log_outputs: bool = False,
):
    """
    The `ClientHandlerDecorator` is a decorator to handle several checks in PolyaxonClient.

     * check_offline: to ignore any decorated function when POLYAXON_IS_OFFLINE env var is found.
     * check_no_op: to ignore any decorated function when NO_OP env var is found.
     * handle_openapi_exceptions: to handle exception of OpenApi and generate better
        debugging outputs.
     * can_log_events: to check if there's an event logger instance on the object.
     * can_log_outputs: to check if there's an outputs path set on the run.
     * openapi_extra_context: to augment openapi errors.

    usage example with class method:
        @client_handler(check_no_op=True)
        def my_func(self, *args, **kwargs):
            ...
            return ...

    usage example with a function:
        @client_handler(check_no_op=True)
        def my_func(arg1, arg2):
            ...
            return ...
    """

    def client_handler_wrapper(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if check_no_op and settings.CLIENT_CONFIG.no_op:
                logger.debug("Using NO_OP mode")
                return None
            if check_offline:
                self_arg = args[0] if args else None
                is_offline = getattr(self_arg, "_is_offline", None)
                if (
                    is_offline
                    if is_offline is not None
                    else settings.CLIENT_CONFIG.is_offline
                ):
                    logger.debug("Using IS_OFFLINE mode")
                    return None
            if args:
                self_arg = args[0]

                if can_log_events and (
                    not hasattr(self_arg, "_event_logger")
                    or self_arg._event_logger is None  # pylint:disable=protected-access
                ):
                    logger.warning(
                        "You should set an event logger before calling: {}".format(
                            f.__name__
                        )
                    )

                if can_log_outputs and (
                    not hasattr(self_arg, "_outputs_path")
                    or self_arg._outputs_path is None  # pylint:disable=protected-access
                ):
                    logger.warning(
                        "You should set an an outputs path before calling: {}".format(
                            f.__name__
                        )
                    )

            try:
                return f(*args, **kwargs)
            except (ApiException, HTTPError) as e:
                logger.debug("Client config:\n%s\n", settings.CLIENT_CONFIG.to_dict())
                raise e

        return wrapper

    return client_handler_wrapper
