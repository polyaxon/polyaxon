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

import six

from hestia.list_utils import to_list


def validate_tags(tags):
    if not tags:
        return None

    if isinstance(tags, six.string_types):
        tags = [tag.strip() for tag in tags.split(",")]
    tags = to_list(tags)
    tags = [tag for tag in tags if (tag and isinstance(tag, six.string_types))]
    return tags
