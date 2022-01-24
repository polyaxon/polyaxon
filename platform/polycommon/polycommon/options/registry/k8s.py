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

from polyaxon import types
from polycommon.options.option import Option, OptionScope, OptionStores

K8S_NAMESPACE = "K8S_NAMESPACE"
K8S_IN_CLUSTER = "K8S_IN_CLUSTER"

OPTIONS = {K8S_NAMESPACE, K8S_IN_CLUSTER}


class K8SNamespace(Option):
    key = K8S_NAMESPACE
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    typing = types.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SInCluster(Option):
    key = K8S_IN_CLUSTER
    scope = OptionScope.GLOBAL
    is_secret = False
    is_optional = False
    is_list = False
    typing = types.BOOL
    store = OptionStores.SETTINGS
    default = None
    options = None
