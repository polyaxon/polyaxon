#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from typing import Optional, Tuple

from django.conf import settings

from polyaxon import types
from polycommon.options.exceptions import OptionException
from polycommon.options.option import (
    NAMESPACE_DB_OPTION_MARKER,
    Option,
    OptionScope,
    OptionStores,
)
from polycommon.options.option_namespaces import FEATURES


class Feature(Option):
    scope = OptionScope.USER
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores(settings.STORE_OPTION)
    typing = types.BOOL
    default = True
    options = [True, False]
    immutable = False  # If immutable, the feature cannot be update by the user
    description = None

    @classmethod
    def get_marker(cls) -> str:
        return NAMESPACE_DB_OPTION_MARKER

    @classmethod
    def parse_key(cls) -> Tuple[Optional[str], str]:
        marker = cls.get_marker()
        parts = cls.key.split(marker)
        # First part is a Meta namespace `features`
        if len(parts) > 3 or len(parts) < 1:  # pylint:disable=len-as-condition
            raise OptionException(
                "Feature declared with multi-namespace key `{}`.".format(cls.key)
            )
        if parts[0] != FEATURES:
            raise OptionException(
                "Feature declared with wrong namespace key `{}`.".format(cls.key)
            )
        if len(parts) == 2:
            return None, parts[1]
        return parts[1], parts[2]

    @classmethod
    def get_namespace(cls) -> Optional[str]:
        return cls.parse_key()[0]

    @classmethod
    def get_key_subject(cls):
        return cls.parse_key()[1]
