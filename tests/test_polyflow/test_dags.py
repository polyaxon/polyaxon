from unittest import TestCase

from polyaxon_schemas.exceptions import PolyaxonSchemaError
from polyaxon_schemas.polyflow import dags


class TestDags(TestCase):
    def setUp(self):
        self.dag0 = (
            (1, {2, 3, 4, 19}),
            (2, {3}),
            (5, {3}),
            (4, set([])),
            (6, set([])),
        )
        self.dag0_processed = dags.process_dag(self.dag0)
        self.dag1 = (
            (1, {2, 3, 4}),
            (2, {3}),
            (5, {3}),
            (4, set([])),
            (6, set([])),
        )
        self.dag1_processed = dags.process_dag(self.dag1)
        self.dag2 = (
            (1, {2, 3, 4}),
            (2, {3}),
            (3, {28}),
            (5, set([])),
            (6, {7, 8}),
            (7, {10}),
            (9, {10, 11}),
        )
        self.dag2_processed = dags.process_dag(self.dag2)
        self.dag3 = (
            (1, {2, 3, 4, 5}),
            (2, {6, 7}),
            (3, {8}),
            (4, {9}),
            (5, {10}),
            (6, {11}),
            (7, set([])),
            (8, {12, 13}),
            (9, {14}),
            (10, {15}),
            (11, set([])),
            (12, set(())),
            (13, set([])),
            (14, set(())),
            (15, set(())),
        )
        self.dag3_processed = dags.process_dag(self.dag3)
        self.dag4 = (
            (0, {1, 2}),
            (1, {2, 3}),
            (2, {3, 5}),
            (3, {4}),
            (4, {6}),
            (6, set([])),
            (5, set([])),
            (7, {6}),
        )
        self.dag4_processed = dags.process_dag(self.dag4)
        self.dag5 = (
            (1, set()),
            (2, {1}),
            (3, {1, 2, 5}),
            (4, {1}),
            (6, set([])),
            (5, set([])),
        )
        self.dag5_processed = dags.process_dag(self.dag5)

        #
        self.cycle1 = (
            (1, {2}),
            (2, {3}),
            (3, {4}),
            (4, {1}),
        )
        self.cycle1_processed = dags.process_dag(self.cycle1)
        self.cycle2 = (
            (1, {2, 3, 4, 5}),
            (2, {3, 1}),
            (3, set([])),
            (4, set([])),
            (5, {2}),
            (6, {7, 8}),
            (7, {10}),
            (9, {10, 11}),
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
        assert dags.sort_topologically(self.dag1_processed, flatten=True) == [3, 4, 6, 2, 5, 1]
        assert dags.sort_topologically(self.dag2_processed, flatten=True) == [4, 5, 8, 10, 11, 28, 3, 7, 9, 2, 6, 1]
        assert dags.sort_topologically(self.dag3_processed, flatten=True) == [7, 11, 12, 13, 14, 15, 6, 8, 9, 10, 2, 3, 4, 5, 1]
        assert dags.sort_topologically(self.dag4_processed, flatten=True) == [5, 6, 7, 4, 3, 2, 1, 0]
        assert dags.sort_topologically(self.dag5_processed, flatten=True) == [1, 5, 6, 2, 4, 3]

        with self.assertRaises(PolyaxonSchemaError):  # Cycles
            assert dags.sort_topologically(self.cycle1_processed)
        with self.assertRaises(PolyaxonSchemaError):  # Cycles
            assert dags.sort_topologically(self.cycle2_processed)
