from pipelines import dags
from tests.utils import BaseTest


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
        assert dags.get_orphan_nodes(self.cycle1) == set([])
        assert dags.get_orphan_nodes(self.cycle2) == set([])

    def test_get_independent_nodes(self):
        assert dags.get_independent_nodes(self.dag1) == {1, 5, 6}
        assert dags.get_independent_nodes(self.dag2) == {1, 5, 6, 9}
        assert dags.get_independent_nodes(self.cycle1) == set([])
        assert dags.get_independent_nodes(self.cycle2) == {6, 9}

    def test_has_dependencies(self):
        assert dags.has_dependencies(node=1, dag=self.dag1) is False
        assert dags.has_dependencies(node=2, dag=self.dag1) is True
        assert dags.has_dependencies(node=1, dag=self.dag2) is False
        assert dags.has_dependencies(node=2, dag=self.dag2) is True
        assert dags.has_dependencies(node=1, dag=self.cycle1) is True
        assert dags.has_dependencies(node=2, dag=self.cycle1) is True
        assert dags.has_dependencies(node=3, dag=self.cycle1) is True
        assert dags.has_dependencies(node=1, dag=self.cycle2) is True
        assert dags.has_dependencies(node=9, dag=self.cycle2) is False

    def test_sort_topologically(self):
        assert dags.sort_topologically(self.dag1) == [1, 2, 4, 5, 6]
        assert dags.sort_topologically(self.dag2) == [1, 2, 3, 5, 6, 7, 9]
        with self.assertRaises(ValueError):  # Cycles
            assert dags.sort_topologically(self.cycle1)
        with self.assertRaises(ValueError):  # Cycles
            assert dags.sort_topologically(self.cycle2)

