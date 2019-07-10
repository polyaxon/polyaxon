import pytest

from conf.cluster_conf_service import ClusterConfService
from conf.exceptions import ConfException
from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from options.feature import Feature
from options.option_manager import OptionManager
from tests.base.case import BaseTest


class DummyDBService(ClusterConfService):

    def __init__(self):
        self.options = set([])
        super().__init__()

    def get(self, key, to_dict=False):
        self.options.add(key)
        return super().get(key, to_dict=to_dict)


class DummyFeature(Feature):
    key = 'FEATURES:FOO'


@pytest.mark.features_mark
class TestFeaturesService(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Cluster.get_or_create_owner(Cluster.load())
        self.db_service = DummyDBService()
        self.db_service.option_manager = OptionManager()
        self.db_service.setup()

    def test_can_handle(self):
        # Test handles only str event types
        assert self.db_service.can_handle(key=1) is False

        with self.assertRaises(ConfException):
            self.db_service.get(key=DummyFeature.key)

        # Subscribe to the event
        self.db_service.option_manager.subscribe(DummyFeature)
        assert self.db_service.can_handle(key=DummyFeature.key) is True

        # Get default value
        assert self.db_service.get(key=DummyFeature.key) is True

        # Update
        ConfigOption.objects.create(owner=self.owner, key=DummyFeature.key, value=False)
        assert self.db_service.get(key=DummyFeature.key) is False
