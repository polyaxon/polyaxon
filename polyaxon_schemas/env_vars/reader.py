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

import os
from typing import Any, List, Set, Union

from polyaxon_schemas.utils.path_utils import check_dirname_exists


def get_from_env(keys: Union[Set[str], List[str], str]) -> Any:
    """
    Returns a variable from one of the list of keys based on the os.env.
    Args:
        keys: list(str). list of keys to check in the environment

    Returns:
        str | None
    """
    keys = keys or []
    if not isinstance(keys, (list, tuple, set)):
        keys = [keys]
    for key in keys:
        value = os.environ.get(key)
        if value:
            if value.lower() == "true":
                return True
            if value.lower() == "false":
                return False
            return value
        # Prepend POLYAXON
        key = "POLYAXON_{}".format(key)
        value = os.environ.get(key)
        if value:
            return value

    return None


def get_from_path(context_path: str, keys: Union[Set[str], List[str], str]) -> Any:
    """
    Returns a variable from one of the list of keys based on a base path.
    Args:
        context_path: str, base path where to look for keys.
        keys: list(str). list of keys to check in the environment

    Returns:
        str | None
    """
    if not check_dirname_exists(context_path, is_dir=True):
        return None

    keys = keys or []
    if not isinstance(keys, (list, tuple)):
        keys = [keys]
    for key in keys:
        key_path = os.path.join(context_path, key)
        if not os.path.exists(key_path):
            return None
        with open(key_path) as f:
            value = f.read()
            if value:
                if value.lower() == "true":
                    return True
                if value.lower() == "false":
                    return False
                return value

    return None


def read_keys(context_path: str, keys: List[str]) -> Any:
    """Returns a variable by checking first a context path and then in the environment."""
    keys = (
        {k.lower() for k in keys}
        | {k.upper() for k in keys}
        | {"".join(k.lower().split("_")) for k in keys}
    )
    if context_path:
        value = get_from_path(context_path=context_path, keys=keys)
        if value is not None:
            return value
    return get_from_env(keys)
