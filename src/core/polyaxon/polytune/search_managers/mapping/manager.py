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

import copy

from typing import Dict, List

from polyaxon.polyflow import V1Mapping
from polyaxon.polytune.search_managers.base import BaseManager


class MappingManager(BaseManager):
    """Mapping strategy manager for running parallel operations."""

    CONFIG = V1Mapping

    def get_suggestions(self, params: Dict = None) -> List[Dict]:
        suggestions = []
        params = params or {}
        for v in self.config.values:
            suggestion_params = copy.deepcopy(params)
            suggestion_params.update(copy.deepcopy(v))
            suggestions.append(suggestion_params)
        return suggestions
