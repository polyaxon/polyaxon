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

from typing import Dict, Optional

from rest_framework import serializers

from coredb.abstracts.runs import BaseRun


class CloningMixin(serializers.Serializer):
    def get_original(self, obj: BaseRun) -> Optional[Dict]:
        if not obj.original_id:
            return None

        return {
            "uuid": obj.original.uuid.hex,
            "name": obj.original.name,
            "kind": obj.cloning_kind,
        }
