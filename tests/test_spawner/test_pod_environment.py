from unittest import TestCase

from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_node_selector,
    get_tolerations
)


class TestPodEnvironment(TestCase):
    def test_pod_affinity(self):
        assert get_affinity(None, None) is None
        assert get_affinity({'foo': 'bar'}, None) == {'foo': 'bar'}
        assert get_affinity(None, '{"foo": "bar"}') == {'foo': 'bar'}
        assert get_affinity({'foo': 'bar'}, '{"foo": "moo"}') == {'foo': 'bar'}

    def get_pod_node_selector(self):
        assert get_node_selector(None, None) is None
        assert get_node_selector({'foo': 'bar'}, None) == {'foo': 'bar'}
        assert get_node_selector(None, '{"foo": "bar"}') == {'foo': 'bar'}
        assert get_node_selector({'foo': 'bar'}, '{"foo": "moo"}') == {'foo': 'bar'}

    def get_pod_tolerations(self):
        assert get_tolerations(None, None) is None
        assert get_tolerations([{'foo': 'bar'}], None) == [{'foo': 'bar'}]
        assert get_tolerations(None, '[{"foo": "bar"}]') == [{'foo': 'bar'}]
        assert get_tolerations([{'foo': 'bar'}], '[{"foo": "moo"}]') == {'foo': 'bar'}
