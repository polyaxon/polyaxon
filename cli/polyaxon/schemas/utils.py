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

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import post_dump, post_load
from marshmallow.utils import _Missing


class UnknownSchemaMixin(object):
    @post_load(pass_original=True)
    def _handle_load_unknown(self, data, original):
        """Preserve unknown keys during deserialization."""
        for key, val in original.items():
            if key not in self.fields:
                data[key] = val
        return data

    @post_dump(pass_original=True)
    def _handle_dump_unknown(self, data, original):
        """Preserve unknown keys during deserialization."""
        for key, val in original.items():
            if key not in self.fields:
                data[key] = val
        return data


missing = _Missing()


def get_value(key, obj, default=missing):
    """Helper for pulling a keyed value off various types of objects"""
    if isinstance(key, int):
        return _get_value_for_key(key, obj, default)
    return _get_value_for_keys(key.split("."), obj, default)


def _get_value_for_keys(keys, obj, default):
    if len(keys) == 1:
        return _get_value_for_key(keys[0], obj, default)
    return _get_value_for_keys(
        keys[1:], _get_value_for_key(keys[0], obj, default), default
    )


def _get_value_for_key(key, obj, default):
    try:
        return obj[key]
    except (KeyError, AttributeError, IndexError, TypeError):
        try:
            attr = getattr(obj, key)
            if callable(attr):
                if hasattr(attr, "get_config") or hasattr(attr, "SCHEMA"):
                    return attr

                return attr.__name__

            return attr
        except AttributeError:
            return default


def to_camel_case(snake_str):
    split_str = snake_str.split("_")
    if len(split_str) == 1:
        try:
            return snake_str if str.isupper(snake_str[0]) else snake_str.title()
        except TypeError:
            return (
                snake_str if six.text_type.isupper(snake_str[0]) else snake_str.title()
            )
    return "".join(x.title() for x in split_str)


class TaskType(object):
    MASTER = "master"
    CHIEF = "chief"
    PS = "ps"
    WORKER = "worker"
    SERVER = "server"
    SCHEDULER = "scheduler"

    VALUES = [MASTER, PS, WORKER, SERVER, SCHEDULER]
