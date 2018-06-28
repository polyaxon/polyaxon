from unittest import TestCase

from django.test import override_settings

from libs.paths.exceptions import VolumeNotFoundError
from scheduler.spawners.templates.volumes import get_pod_volumes


class TestPodVolumes(TestCase):
    PERSISTENCE_OUTPUTS = {
        'outputs1': {
            'mountPath': '/outputs/1',
            'existingClaim': 'test-claim-outputs-1'
        },
        'outputs2': {
            'mountPath': '/outputs/2',
            'hostPath': '/root/outputs'
        }
    }
    PERSISTENCE_DATA = {
        'data1': {
            'mountPath': '/data/1',
            'existingClaim': 'test-claim-data-1'
        },
        'data2': {
            'mountPath': '/data/2',
            'hostPath': '/root/data'
        }
    }

    def test_default_get_pod_volumes(self):
        volumes, volume_mounts = get_pod_volumes(persistence_outputs=None, persistence_data=None)
        assert len(volumes) == 2
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs'
        assert volumes[1].persistent_volume_claim.claim_name == 'test-claim-data'

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS, PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_pod_volumes_changes(self):
        volumes, volume_mounts = get_pod_volumes(persistence_outputs=None, persistence_data=None)
        assert len(volumes) == 3
        if volumes[0].name == 'outputs1':
            assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs-1'
            assert volume_mounts[0].mount_path == '/outputs/1'
        elif volumes[0].name == 'outputs2':
            assert volumes[0].host_path.path == '/root/outputs'
            assert volume_mounts[0].mount_path == '/outputs/2'

        data_claim_name = None
        data_host_path = None
        mount_path1 = None
        mount_path2 = None
        if volumes[1].name == 'data1':
            data_claim_name = volumes[1].persistent_volume_claim.claim_name
            data_host_path = volumes[2].host_path.path
            mount_path1 = volume_mounts[1].mount_path
            mount_path2 = volume_mounts[2].mount_path
        elif volumes[1].name == 'data2':
            data_host_path = volumes[1].host_path.path
            data_claim_name = volumes[2].persistent_volume_claim.claim_name
            mount_path2 = volume_mounts[1].mount_path
            mount_path1 = volume_mounts[2].mount_path

        assert data_claim_name == 'test-claim-data-1'
        assert data_host_path == '/root/data'
        assert mount_path1 == '/data/1'
        assert mount_path2 == '/data/2'

        with self.assertRaises(VolumeNotFoundError):
            get_pod_volumes(persistence_outputs='foo', persistence_data=None)

        with self.assertRaises(VolumeNotFoundError):
            get_pod_volumes(persistence_outputs=None, persistence_data='foo')

        volumes, volume_mounts = get_pod_volumes(persistence_outputs='outputs2',
                                                 persistence_data=['data2'])
        assert len(volumes) == 2
        assert volumes[0].host_path.path == '/root/outputs'
        assert volumes[1].host_path.path == '/root/data'
        assert volume_mounts[0].mount_path == '/outputs/2'
        assert volume_mounts[1].mount_path == '/data/2'

        volumes, volume_mounts = get_pod_volumes(persistence_outputs='outputs1',
                                                 persistence_data=['data1', 'data2'])
        assert len(volumes) == 3
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs-1'

        data_claim_name = None
        data_host_path = None
        mount_path1 = None
        mount_path2 = None
        if volumes[1].name == 'data1':
            data_claim_name = volumes[1].persistent_volume_claim.claim_name
            data_host_path = volumes[2].host_path.path
            mount_path1 = volume_mounts[1].mount_path
            mount_path2 = volume_mounts[2].mount_path
        elif volumes[1].name == 'data2':
            data_host_path = volumes[1].host_path.path
            data_claim_name = volumes[2].persistent_volume_claim.claim_name
            mount_path2 = volume_mounts[1].mount_path
            mount_path1 = volume_mounts[2].mount_path

        assert data_claim_name == 'test-claim-data-1'
        assert data_host_path == '/root/data'
        assert mount_path1 == '/data/1'
        assert mount_path2 == '/data/2'
