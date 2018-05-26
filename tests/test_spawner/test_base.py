# -*- coding: utf-8 -*-
from unittest import TestCase

from runner.spawners.base import get_pod_volumes
from django.conf import settings

class TestBase(TestCase):
    def test_get_pod_volumes(self):
        settings.DATA_CLAIM_NAME = 'test-claim-data'
        settings.OUTPUTS_CLAIM_NAME = 'test-claim-outputs'
        volumes, volume_mounts = get_pod_volumes()
        assert len(volumes) == 2
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-data'
        assert volumes[1].persistent_volume_claim.claim_name == 'test-claim-outputs'

        settings.DATA_CLAIM_NAME = 'test-claim-data'
        settings.OUTPUTS_CLAIM_NAME = 'test-claim-outputs'
        settings.EXTRA_PERSISTENCES = [{
            'mountPath': '/storage/1',
            'existingClaim': 'test-claim-extra-1'
        }, {
            'mountPath': '/storage/2',
            'hostPath': '/root/test'
        }]
        volumes, volume_mounts = get_pod_volumes()
        assert len(volumes) == 4
        assert volumes[0].persistent_volume_claim.claim_name == 'test-claim-data'
        assert volumes[1].persistent_volume_claim.claim_name == 'test-claim-outputs'
        assert volumes[2].persistent_volume_claim.claim_name == 'test-claim-extra-1'
        assert volumes[3].host_path.path == '/root/test'
        assert volume_mounts[2].mount_path == '/storage/1'
        assert volume_mounts[3].mount_path == '/storage/2'

