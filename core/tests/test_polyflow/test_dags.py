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

from mock import MagicMock

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyflow import dags
from tests.utils import BaseTestCase


@pytest.mark.polyflow_mark
class TestDags(BaseTestCase):
    def setUp(self):
        self.dag0 = (
            (MagicMock(id=1), {2, 3, 4, 19}),
            (MagicMock(id=2), {3}),
            (MagicMock(id=5), {3}),
            (MagicMock(id=4), set([])),
            (MagicMock(id=6), set([])),
        )
        self.dag0_processed = dags.process_dag(self.dag0)
        self.dag1 = (
            (MagicMock(id=1), {2, 3, 4}),
            (MagicMock(id=2), {3}),
            (MagicMock(id=5), {3}),
            (MagicMock(id=4), set([])),
            (MagicMock(id=6), set([])),
        )
        self.dag1_processed = dags.process_dag(self.dag1)
        self.dag2 = (
            (MagicMock(id=1), {2, 3, 4}),
            (MagicMock(id=2), {3}),
            (MagicMock(id=3), {28}),
            (MagicMock(id=5), set([])),
            (MagicMock(id=6), {7, 8}),
            (MagicMock(id=7), {10}),
            (MagicMock(id=9), {10, 11}),
        )
        self.dag2_processed = dags.process_dag(self.dag2)
        self.dag3 = (
            (MagicMock(id=1), {2, 3, 4, 5}),
            (MagicMock(id=2), {6, 7}),
            (MagicMock(id=3), {8}),
            (MagicMock(id=4), {9}),
            (MagicMock(id=5), {10}),
            (MagicMock(id=6), {11}),
            (MagicMock(id=7), set([])),
            (MagicMock(id=8), {12, 13}),
            (MagicMock(id=9), {14}),
            (MagicMock(id=10), {15}),
            (MagicMock(id=11), set([])),
            (MagicMock(id=12), set(())),
            (MagicMock(id=13), set([])),
            (MagicMock(id=14), set(())),
            (MagicMock(id=15), set(())),
        )
        self.dag3_processed = dags.process_dag(self.dag3)
        self.dag4 = (
            (MagicMock(id=0), {1, 2}),
            (MagicMock(id=1), {2, 3}),
            (MagicMock(id=2), {3, 5}),
            (MagicMock(id=3), {4}),
            (MagicMock(id=4), {6}),
            (MagicMock(id=6), set([])),
            (MagicMock(id=5), set([])),
            (MagicMock(id=7), {6}),
        )
        self.dag4_processed = dags.process_dag(self.dag4)
        self.dag5 = (
            (MagicMock(id=1), set()),
            (MagicMock(id=2), {1}),
            (MagicMock(id=3), {1, 2, 5}),
            (MagicMock(id=4), {1}),
            (MagicMock(id=6), set([])),
            (MagicMock(id=5), set([])),
        )
        self.dag5_processed = dags.process_dag(self.dag5)

        #
        self.cycle1 = (
            (MagicMock(id=1), {2}),
            (MagicMock(id=2), {3}),
            (MagicMock(id=3), {4}),
            (MagicMock(id=4), {1}),
        )
        self.cycle1_processed = dags.process_dag(self.cycle1)
        self.cycle2 = (
            (MagicMock(id=1), {2, 3, 4, 5}),
            (MagicMock(id=2), {3, 1}),
            (MagicMock(id=3), set([])),
            (MagicMock(id=4), set([])),
            (MagicMock(id=5), {2}),
            (MagicMock(id=6), {7, 8}),
            (MagicMock(id=7), {10}),
            (MagicMock(id=9), {10, 11}),
        )
        self.cycle2_processed = dags.process_dag(self.cycle2)
        return super().setUp()

    def test_get_orphan_nodes(self):
        assert dags.get_orphan_ops(self.dag0_processed) == {3, 19}
        assert dags.get_orphan_ops(self.dag1_processed) == {3}
        assert dags.get_orphan_ops(self.dag2_processed) == {4, 8, 10, 11, 28}
        assert dags.get_orphan_ops(self.dag3_processed) == set([])
        assert dags.get_orphan_ops(self.dag4_processed) == set([])
        assert dags.get_orphan_ops(self.dag5_processed) == set([])
        assert dags.get_orphan_ops(self.cycle1_processed) == set([])
        assert dags.get_orphan_ops(self.cycle2_processed) == {8, 10, 11}

    def test_get_independent_ops(self):
        assert dags.get_independent_ops(self.dag0_processed) == {3, 4, 6, 19}
        assert dags.get_independent_ops(self.dag1_processed) == {3, 4, 6}
        assert dags.get_independent_ops(self.dag2_processed) == {4, 5, 8, 10, 11, 28}
        assert dags.get_independent_ops(self.dag3_processed) == {7, 11, 12, 13, 14, 15}
        assert dags.get_independent_ops(self.dag4_processed) == {5, 6}
        assert dags.get_independent_ops(self.dag5_processed) == {6, 5, 1}
        assert dags.get_independent_ops(self.cycle1_processed) == set([])
        assert dags.get_independent_ops(self.cycle2_processed) == {3, 4, 8, 10, 11}

    def test_has_dependencies(self):
        assert dags.has_dependencies(op=19, dag=self.dag0_processed) is False
        assert dags.has_dependencies(op=2, dag=self.dag0_processed) is True
        assert dags.has_dependencies(op=1, dag=self.dag1_processed) is True
        assert dags.has_dependencies(op=2, dag=self.dag1_processed) is True
        assert dags.has_dependencies(op=1, dag=self.dag2_processed) is True
        assert dags.has_dependencies(op=2, dag=self.dag2_processed) is True
        assert dags.has_dependencies(op=5, dag=self.dag2_processed) is False
        assert dags.has_dependencies(op=1, dag=self.dag3_processed) is True
        assert dags.has_dependencies(op=7, dag=self.dag3_processed) is False
        assert dags.has_dependencies(op=12, dag=self.dag3_processed) is False
        assert dags.has_dependencies(op=1, dag=self.dag5_processed) is False
        assert dags.has_dependencies(op=1, dag=self.cycle1_processed) is True
        assert dags.has_dependencies(op=2, dag=self.cycle1_processed) is True
        assert dags.has_dependencies(op=3, dag=self.cycle1_processed) is True
        assert dags.has_dependencies(op=1, dag=self.cycle2_processed) is True
        assert dags.has_dependencies(op=9, dag=self.cycle2_processed) is True
        assert dags.has_dependencies(op=11, dag=self.cycle2_processed) is False

    def test_sort_topologically(self):
        assert dags.sort_topologically(self.dag1_processed, flatten=True) == [
            3,
            4,
            6,
            2,
            5,
            1,
        ]
        assert dags.sort_topologically(self.dag2_processed, flatten=True) == [
            4,
            5,
            8,
            10,
            11,
            28,
            3,
            7,
            9,
            2,
            6,
            1,
        ]
        assert dags.sort_topologically(self.dag3_processed, flatten=True) == [
            7,
            11,
            12,
            13,
            14,
            15,
            6,
            8,
            9,
            10,
            2,
            3,
            4,
            5,
            1,
        ]
        assert dags.sort_topologically(self.dag4_processed, flatten=True) == [
            5,
            6,
            7,
            4,
            3,
            2,
            1,
            0,
        ]
        assert dags.sort_topologically(self.dag5_processed, flatten=True) == [
            1,
            5,
            6,
            2,
            4,
            3,
        ]

        with self.assertRaises(PolyaxonSchemaError):  # Cycles
            assert dags.sort_topologically(self.cycle1_processed)
        with self.assertRaises(PolyaxonSchemaError):  # Cycles
            assert dags.sort_topologically(self.cycle2_processed)
