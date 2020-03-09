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

from kubernetes.client import Configuration

from polyaxon import settings
from polyaxon.exceptions import PolyaxonAgentError
from polyaxon.polypod.mixins import MIXIN_MAPPING, BaseMixin


class BaseSpawner:
    def __init__(
        self,
        namespace: str = None,
        k8s_config: Configuration = None,
        in_cluster: bool = None,
    ):
        if in_cluster is None:
            in_cluster = settings.CLIENT_CONFIG.in_cluster

        if not namespace:
            namespace = settings.CLIENT_CONFIG.namespace

        self.namespace = namespace
        self.in_cluster = in_cluster
        self.k8s_config = k8s_config
        self._k8s_manager = None

    @staticmethod
    def _get_mixin_for_kind(kind: str) -> BaseMixin:
        m = MIXIN_MAPPING.get(kind)
        if not m:
            raise PolyaxonAgentError("Agent received unrecognized kind {}".format(kind))
        return m

    @property
    def k8s_manager(self):
        raise NotImplementedError
