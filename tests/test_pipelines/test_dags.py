import pytest

from factories.factory_pipelines import OperationFactory
from pipelines import dags
from tests.utils import BaseTest


@pytest.mark.pipelines_mark
class TestDags(BaseTest):
    def setUp(self):

        self.dag1 = {
            1: [2, 3, 4],
            2: [3],
            5: [3],
            4: [],
            6: []
        }
        self.dag2 = {
            1: [2, 3, 4],
            2: [3],
            3: [],
            5: [],
            6: [7, 8],
            7: [10],
            9: [10, 11],
        }
        self.dag3 = {
            1: [2, 3, 4, 5],
            2: [6, 7],
            3: [8],
            4: [9],
            5: [10],
            6: [11],
            7: [],
            8: [12, 13],
            9: [14],
            10: [15],
            11: [],
            12: []
        }
        self.dag4 = {
            0: [1, 2],
            1: [2, 3],
            2: [3, 5],
            3: [4],
            5: [],
            7: [6]
        }
        #
        self.cycle1 = {
            1: [2],
            2: [3],
            3: [4],
            4: [1],
        }
        self.cycle2 = {
            1: [2, 3, 4, 5],
            2: [3, 1],
            5: [2],
            6: [7, 8],
            7: [10],
            9: [10, 11],
        }
        return super().setUp()

    def test_get_orphan_nodes(self):
        assert dags.get_orphan_nodes(self.dag1) == {6, }
        assert dags.get_orphan_nodes(self.dag2) == {5, }
        assert dags.get_orphan_nodes(self.dag3) == set([])
        assert dags.get_orphan_nodes(self.dag4) == set([])
        assert dags.get_orphan_nodes(self.cycle1) == set([])
        assert dags.get_orphan_nodes(self.cycle2) == set([])

    def test_get_independent_nodes(self):
        assert dags.get_independent_nodes(self.dag1) == {1, 5, 6}
        assert dags.get_independent_nodes(self.dag2) == {1, 5, 6, 9}
        assert dags.get_independent_nodes(self.dag3) == {1}
        assert dags.get_independent_nodes(self.dag4) == {0, 7}
        assert dags.get_independent_nodes(self.cycle1) == set([])
        assert dags.get_independent_nodes(self.cycle2) == {6, 9}

    def test_has_dependencies(self):
        assert dags.has_dependencies(node=1, dag=self.dag1) is False
        assert dags.has_dependencies(node=2, dag=self.dag1) is True
        assert dags.has_dependencies(node=1, dag=self.dag2) is False
        assert dags.has_dependencies(node=2, dag=self.dag2) is True
        assert dags.has_dependencies(node=1, dag=self.dag3) is False
        assert dags.has_dependencies(node=2, dag=self.dag3) is True
        assert dags.has_dependencies(node=10, dag=self.dag3) is True
        assert dags.has_dependencies(node=1, dag=self.cycle1) is True
        assert dags.has_dependencies(node=2, dag=self.cycle1) is True
        assert dags.has_dependencies(node=3, dag=self.cycle1) is True
        assert dags.has_dependencies(node=1, dag=self.cycle2) is True
        assert dags.has_dependencies(node=9, dag=self.cycle2) is False

    def test_sort_topologically(self):
        assert dags.sort_topologically(self.dag1) == [1, 5, 6, 2, 4]
        assert dags.sort_topologically(self.dag2) == [1, 5, 6, 9, 2, 7, 3]
        assert dags.sort_topologically(self.dag3) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert dags.sort_topologically(self.dag4) == [0, 7, 1, 2, 3, 5]

        with self.assertRaises(ValueError):  # Cycles
            assert dags.sort_topologically(self.cycle1)
        with self.assertRaises(ValueError):  # Cycles
            assert dags.sort_topologically(self.cycle2)

    def test_get_dag(self):
        operations = [OperationFactory() for _ in range(4)]
        operations[0].upstream_operations.set(operations[2:])
        operations[1].upstream_operations.set(operations[2:])
        operation_by_ids = {op.id: op for op in operations}

        def get_downstream(op):
            return op.downstream_operations.values_list('id', flat=True)

        assert dags.get_dag(nodes=operations, downstream_fn=get_downstream) == (
            {
                operations[0].id: set(),
                operations[1].id: set(),
                operations[2].id: {operations[0].id, operations[1].id},
                operations[3].id: {operations[0].id, operations[1].id},
            },
            operation_by_ids
        )

        # Add operations outside the dag
        operation1 = OperationFactory()
        operation1.downstream_operations.set([operations[1], operations[2], operations[3]])

        operation2 = OperationFactory()
        operation2.upstream_operations.set([operations[0], operations[2]])

        assert dags.get_dag(nodes=operations, downstream_fn=get_downstream) == (
            {
                operations[0].id: {operation2.id, },
                operations[1].id: set(),
                operations[2].id: {operations[0].id, operations[1].id, operation2.id},
                operations[3].id: {operations[0].id, operations[1].id},
            },
            operation_by_ids
        )
