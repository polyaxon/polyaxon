import pytest

from django.test import override_settings

import conf
import encryptor

from encryptor.manager import EncryptionManager
from options.registry.core import ENCRYPTION_KEY, ENCRYPTION_SECRET
from tests.base.case import BaseTest


@pytest.mark.encryption_mark
class TestEncryptor(BaseTest):

    def test_default_encryption(self):
        assert conf.get(ENCRYPTION_KEY) is None
        assert conf.get(ENCRYPTION_SECRET) is None

        assert encryptor.encrypt('foo') == 'foo'
        assert encryptor.decrypt('foo') == 'foo'

    @override_settings(ENCRYPTION_KEY='my_key',
                       ENCRYPTION_SECRET='qMGwKR21SAjprV0XOJUI4SoI-MLFoTxN1ahZndKREL4=')
    def test_secret_encryption(self):
        assert conf.get(ENCRYPTION_KEY) == 'my_key'
        assert conf.get(ENCRYPTION_SECRET) == 'qMGwKR21SAjprV0XOJUI4SoI-MLFoTxN1ahZndKREL4='
        encryptor.validate()
        encryptor.setup()

        value = 'foo'
        encrypted_value = encryptor.encrypt(value)

        assert encrypted_value.startswith('{}my_key$'.format(EncryptionManager.MARKER))
        assert encryptor.decrypt(encrypted_value) == 'foo'
