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

import pytest

from polyaxon.polyflow import V1MatrixKind
from tests.utils import BaseTestCase


@pytest.mark.polytune_mark
class TestKinds(BaseTestCase):
    def test_supported_kinds(self):
        assert len(V1MatrixKind.allowable_values) == 7

    def test_eager_kinds(self):
        assert V1MatrixKind.eager_values == {
            V1MatrixKind.MAPPING,
            V1MatrixKind.GRID,
            V1MatrixKind.RANDOM,
        }

    def test_iteration_values(self):
        assert V1MatrixKind.iteration_values == {
            V1MatrixKind.HYPERBAND,
            V1MatrixKind.BAYES,
            V1MatrixKind.HYPEROPT,
            V1MatrixKind.ITERATIVE,
        }
