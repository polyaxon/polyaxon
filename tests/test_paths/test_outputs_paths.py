import pytest

from django.conf import settings
from django.test import override_settings

import stores

from stores.exceptions import VolumeNotFoundError
from stores.validators import validate_persistence_outputs
from tests.utils import BaseTest


@pytest.mark.paths_mark
class TestOutputsPaths(BaseTest):
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

    def test_validate_persistence_outputs(self):
        with self.assertRaises(VolumeNotFoundError):
            validate_persistence_outputs(['path1', 'path2'])

        assert validate_persistence_outputs('path2') == 'path2'
        assert validate_persistence_outputs(None) == list(settings.PERSISTENCE_OUTPUTS.keys())[0]

    def test_get_outputs_paths_raises_for_unrecognised_paths(self):
        with self.assertRaises(VolumeNotFoundError):
            stores.get_outputs_paths(['path1', 'path2'])

    @override_settings(PERSISTENCE_OUTPUTS=PERSISTENCE_OUTPUTS)
    def test_get_outputs_paths_works_as_expected(self):
        with self.assertRaises(VolumeNotFoundError):
            stores.get_outputs_paths('path1')

        assert stores.get_outputs_paths('outputs2') == '/outputs/2'
        assert stores.get_outputs_paths('outputs3') == 'gs://output-bucket'
