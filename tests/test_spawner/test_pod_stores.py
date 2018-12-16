from unittest import TestCase

import pytest

from django.test import override_settings

from db.models.outputs import OutputsRefsSpec
from scheduler.spawners.templates.stores import (
    get_data_store_secrets,
    get_outputs_refs_store_secrets,
    get_outputs_store_secrets
)
from stores.exceptions import VolumeNotFoundError


@pytest.mark.spawner_mark
class TestPodStores(TestCase):
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
            'secret': 'outputs-secret-name',
            'secretKey': 'outputs-secret-key'
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
            'bucket': 'gs://data3-bucket',
            'secret': 'data3-secret-name',
            'secretKey': 'data3-secret-key'
        },
        'data4': {
            'store': 'gcs',
            'bucket': 'gs://data4-bucket',
            'secret': 'data4-secret-name',
            'secretKey': 'data4-secret-key'
        }
    }

    def test_get_outputs_store_secrets(self):
        secrets, _ = get_outputs_store_secrets('outputs', '/path')
        self.assertEqual(len(secrets), 0)
        secrets, _ = get_outputs_store_secrets(None, None)
        self.assertEqual(len(secrets), 0)
        with self.assertRaises(VolumeNotFoundError):
            get_outputs_store_secrets('outputs1', '/path')

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_outputs_store_secrets_with_updated_settings(self):
        with self.assertRaises(VolumeNotFoundError):
            get_outputs_store_secrets('outputs', '/path')

        secrets, _ = get_outputs_store_secrets('outputs1', '/path/to/outputs')
        self.assertEqual(len(secrets), 0)

        secrets, secret_keys = get_outputs_store_secrets('outputs3', '/path/to/outputs')
        assert len(secrets) == 1
        assert len(secret_keys) == 1
        assert list(secrets)[0] == ('outputs-secret-name', 'outputs-secret-key')
        assert secret_keys == {
            '/path/to/outputs': {'secret_key': 'outputs-secret-key', 'store': 'gcs'}}

    def test_get_data_store_secrets(self):
        secrets, _ = get_data_store_secrets(['data'], {})
        self.assertEqual(len(secrets), 0)
        secrets, _ = get_data_store_secrets(None, None)
        self.assertEqual(len(secrets), 0)
        with self.assertRaises(VolumeNotFoundError):
            get_data_store_secrets(['data1'], {})

    @override_settings(PERSISTENCE_DATA=PERSISTENCE_DATA)
    def test_get_data_store_secrets_with_updated_settings(self):
        with self.assertRaises(VolumeNotFoundError):
            get_data_store_secrets(['data'], {})

        secrets, _ = get_data_store_secrets(['data1'], {'data1': '/path/to/data'})
        self.assertEqual(len(secrets), 0)

        secrets, secret_keys = get_data_store_secrets(['data3'], {'data3': '/path/to/data3'})
        assert len(secrets) == 1
        assert len(secret_keys) == 1
        assert list(secrets)[0] == ('data3-secret-name', 'data3-secret-key')
        assert secret_keys == {
            '/path/to/data3': {'secret_key': 'data3-secret-key', 'store': 'gcs'}}

        secrets, secret_keys = get_data_store_secrets(
            ['data3', 'data4'],
            {'data3': '/path/to/data3', 'data4': '/path/to/data4'})
        assert len(secrets) == 2
        assert len(secret_keys) == 2
        assert secrets == {
            ('data3-secret-name', 'data3-secret-key'),
            ('data4-secret-name', 'data4-secret-key')}
        assert secret_keys == {
            '/path/to/data3': {'secret_key': 'data3-secret-key', 'store': 'gcs'},
            '/path/to/data4': {'secret_key': 'data4-secret-key', 'store': 'gcs'}
        }

    def test_get_outputs_refs_store_secrets(self):
        secrets, _ = get_outputs_refs_store_secrets(None)
        self.assertEqual(len(secrets), 0)
        secrets, _ = get_outputs_refs_store_secrets([
            OutputsRefsSpec(path='/path1', persistence='outputs')])
        self.assertEqual(len(secrets), 0)
        with self.assertRaises(VolumeNotFoundError):
            get_outputs_refs_store_secrets([
                OutputsRefsSpec(path='/path1', persistence='outputs1'),
                OutputsRefsSpec(path='/path2', persistence='outputs2')])

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_outputs_refs_store_secrets_with_updated_settings(self):
        secrets, _ = get_outputs_refs_store_secrets([
            OutputsRefsSpec(path='/path1', persistence='outputs1'),
            OutputsRefsSpec(path='/path2', persistence='outputs2')])
        self.assertEqual(len(secrets), 0)

        secrets, secret_keys = get_outputs_refs_store_secrets([
            OutputsRefsSpec(path='/path1', persistence='outputs3'),
            OutputsRefsSpec(path='/path2', persistence='outputs3')])
        assert len(secrets) == 1
        assert len(secret_keys) == 2
