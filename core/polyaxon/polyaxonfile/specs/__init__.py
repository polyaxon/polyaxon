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

from collections.abc import Mapping

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.polyaxonfile.specs import kinds as spec_kinds
from polyaxon.polyaxonfile.specs.base import BaseSpecification
from polyaxon.polyaxonfile.specs.compiled_operation import (
    CompiledOperationSpecification,
)
from polyaxon.polyaxonfile.specs.component import ComponentSpecification
from polyaxon.polyaxonfile.specs.operation import OperationSpecification

SPECIFICATION_BY_KIND = {
    spec_kinds.OPERATION: OperationSpecification,
    spec_kinds.COMPILED_OPERATION: CompiledOperationSpecification,
    spec_kinds.COMPONENT: ComponentSpecification,
}


def get_specification(data):
    if not isinstance(data, Mapping):
        data = ConfigSpec.read_from(data)
    kind = BaseSpecification.get_kind(data=data)
    return SPECIFICATION_BY_KIND[kind].read(data)
