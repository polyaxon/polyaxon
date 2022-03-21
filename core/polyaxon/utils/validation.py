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

from polyaxon.utils.list_utils import to_list


def validate_tags(tags, validate_yaml: bool = False):
    if not tags:
        return None

    if validate_yaml and isinstance(tags, str) and ("[" in tags and "]" in tags):
        import yaml

        tags = yaml.safe_load(tags)

    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",")]
    tags = to_list(tags, to_unique=True)
    tags = [tag.strip() for tag in tags if (tag and isinstance(tag, str))]
    return [t for t in tags if t]
