import datetime

from clusters.models import Cluster
from tests.utils import BaseTest


class TestClusterModel(BaseTest):
    def test_loads_works(self):
        assert Cluster.load() is not None

    def test_update_works(self):
        cluster = Cluster.load()

        updated_cluster = Cluster.load()
        cluster.version_api = {
            'build_date': datetime.datetime.now().isoformat(),
            'compiler': 'gc',
            'git_commit': '17d7182a7ccbb167074be7a87f0a68bd00d58d91',
            'git_tree_state': 'clean',
            'git_version': 'v1.7.5',
            'go_version': 'go1.8.3',
            'major': '1',
            'minor': '7',
            'platform': 'linux/amd64'
        }
        updated_cluster.save()

        loaded_version = Cluster.load()
        assert loaded_version.version_api != cluster.version_api
        assert loaded_version.version_api == updated_cluster.version_api
