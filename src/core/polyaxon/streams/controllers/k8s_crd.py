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

from polyaxon.k8s.async_manager import AsyncK8SManager
from polyaxon.k8s.custom_resources import operation as op_crd


async def get_k8s_operation(k8s_manager: AsyncK8SManager, resource_name: str):
    return await k8s_manager.get_custom_object(
        name=resource_name,
        group=op_crd.GROUP,
        version=op_crd.API_VERSION,
        plural=op_crd.PLURAL,
    )
