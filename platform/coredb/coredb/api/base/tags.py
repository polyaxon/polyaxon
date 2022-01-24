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

from typing import Dict, List, Optional


class TagsMixin:
    @staticmethod
    def validated_tags(validated_data: Dict, tags: Optional[List[str]]):
        new_tags = validated_data.get("tags")

        if new_tags:
            new_tags = list(set(new_tags))
            validated_data["tags"] = new_tags

        if not validated_data.get("merge") or not tags or not new_tags:
            # This is the default behavior
            return validated_data

        new_tags = tags + [tag for tag in new_tags if tag not in tags]
        validated_data["tags"] = new_tags
        return validated_data
