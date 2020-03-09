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

from typing import Dict, Optional, Union

from polyaxon.k8s import k8s_schemas


def sanitize_resources(
    resources: Union[k8s_schemas.V1ResourceRequirements, Dict]
) -> Optional[k8s_schemas.V1ResourceRequirements]:
    def validate_resources(r_field: Dict) -> Dict:
        if not r_field:
            return r_field

        for k in r_field:
            r_field[k] = str(r_field[k])

        return r_field

    if not resources:
        return None

    if isinstance(resources, Dict):
        return k8s_schemas.V1ResourceRequirements(
            limits=validate_resources(resources.get("limits", None)),
            requests=validate_resources(resources.get("requests", None)),
        )
    else:
        return k8s_schemas.V1ResourceRequirements(
            limits=validate_resources(resources.limits),
            requests=validate_resources(resources.requests),
        )
