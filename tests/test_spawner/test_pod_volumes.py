from unittest import TestCase

import pytest

from django.test import override_settings

from db.models.outputs import OutputsRefsSpec
from stores.exceptions import VolumeNotFoundError
from scheduler.spawners.templates.volumes import (
    get_pod_data_volume,
    get_pod_outputs_volume,
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes
)


@pytest.mark.spawner_mark
class TestPodVolumes(TestCase):
    PERSISTENCE_OUTPUTS = {
        'outputs1': {
            'mountPath': '/outputs/1',
            'existingClaim': 'test-claim-outputs-1'
        },
        'outputs2': {
            'mountPath': '/outputs/2',
            'hostPath': '/root/outputs'
        },
        'outputs3': {
            'store': 'gcs',
            'bucket': 'gs://output-bucket',
            'secret': 'secret-name',
            'secretKey': 'secret-key'
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
        },
        'data3': {
            'store': 'gcs',
            'bucket': 'gs://data-bucket',
            'secret': 'secret-name',
            'secretKey': 'secret-key'
        }
    }

    def test_get_pod_outputs_volume(self):
        volumes, _ = get_pod_outputs_volume(None)
        assert len(volumes) == 1
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs'

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_pod_outputs_volume_wrong_values(self):
        with self.assertRaises(VolumeNotFoundError):
            get_pod_outputs_volume(persistence_outputs='foo')

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_pod_outputs_volume_update_settings(self):
        volumes, _ = get_pod_outputs_volume(persistence_outputs='outputs1')
        assert len(volumes) == 1
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs-1'

        volumes, _ = get_pod_outputs_volume(persistence_outputs='outputs2')
        assert len(volumes) == 1
        assert volumes[0].host_path.path == '/root/outputs'

        volumes, _ = get_pod_outputs_volume(persistence_outputs='outputs3')
        self.assertEqual(len(volumes), 0)

    def test_get_pod_data_volumes(self):
        volumes, _ = get_pod_data_volume(None)
        assert len(volumes) == 1
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-data'

    @override_settings(PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_pod_data_volumes_wrong_values(self):
        with self.assertRaises(VolumeNotFoundError):
            get_pod_data_volume(persistence_data=['foo'])

    @override_settings(PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_pod_data_volumes_update_settings(self):
        volumes, _ = get_pod_data_volume(persistence_data=['data1'])
        assert len(volumes) == 1
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-data-1'

        volumes, _ = get_pod_data_volume(persistence_data=['data2'])
        assert len(volumes) == 1
        assert volumes[0].host_path.path == '/root/data'

        volumes, _ = get_pod_data_volume(persistence_data=['data3'])
        self.assertEqual(len(volumes), 0)

    def test_default_get_pod_volumes(self):
        volumes, _ = get_pod_volumes(persistence_outputs=None, persistence_data=None)
        assert len(volumes) == 2
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs'
        assert volumes[1].persistent_volume_claim.claim_name == 'test-claim-data'

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS, PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_pod_volumes_raises_for_wrong_values(self):
        with self.assertRaises(VolumeNotFoundError):
            get_pod_volumes(persistence_outputs='foo', persistence_data=None)

        with self.assertRaises(VolumeNotFoundError):
            get_pod_volumes(persistence_outputs=None, persistence_data='foo')

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS, PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_default_get_pod_volumes_with_updated_settings(self):
        volumes, volume_mounts = get_pod_volumes(persistence_outputs='outputs1',
                                                 persistence_data=None)
        assert len(volumes) == 3  # Data3 won't be included because it's a bucket
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

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS, PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_pod_volumes_with_specified_values(self):
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

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_pod_refs_outputs_volumes_same_outputs_persistence(self):
        volumes, _ = get_pod_refs_outputs_volumes(
            [OutputsRefsSpec('/outputs1/some/path', 'outputs1')], 'outputs1')
        self.assertEqual(len(volumes), 0)

        volumes, _ = get_pod_refs_outputs_volumes(
            [OutputsRefsSpec('/outputs2/some/path', 'outputs2')], 'outputs1')
        assert len(volumes) == 1
        assert volumes[0].host_path.path == '/root/outputs'

        volumes, _ = get_pod_refs_outputs_volumes(
            [OutputsRefsSpec('/outputs1/some/path', 'outputs1')], 'outputs2')
        assert len(volumes) == 1
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-outputs-1'

        volumes, _ = get_pod_refs_outputs_volumes(
            [OutputsRefsSpec('/outputs1/some/path', 'outputs3')], 'outputs2')
        self.assertEqual(len(volumes), 0)

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS, PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_pod_volumes_with_buckets_values_only(self):
        volumes, _ = get_pod_volumes(persistence_outputs='outputs3', persistence_data=['data3'])
        self.assertEqual(len(volumes), 0)

    def test_get_shm_volumes(self):
        volumes, volume_mounts = get_shm_volumes()
        assert len(volumes) == len(volume_mounts) == 1
        assert volumes[0].empty_dir.medium == 'Memory'
        assert volume_mounts[0].mount_path == '/dev/shm'
