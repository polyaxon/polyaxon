import pytest

from cryptography.fernet import Fernet

from encryptor.execptions import EncryptionError
from encryptor.manager import EncryptionManager
from tests.base.case import BaseTest


@pytest.mark.encryption_mark
class TestEncryptionManager(BaseTest):

    def test_default_values(self):
        manager = EncryptionManager()
        assert manager.key == EncryptionManager.DEFAULT_KEY
        assert manager.scheme is None

        assert manager.encrypt('foo') == 'foo'
        assert manager.decrypt('foo') == 'foo'

    def test_default_null_secret(self):
        manager = EncryptionManager(key='key1')
        assert manager.key == 'key1'
        assert manager.scheme is None

        assert manager.encrypt('foo') == 'foo'
        assert manager.decrypt('foo') == 'foo'

    def test_default_wrong_secret(self):
        with self.assertRaises(EncryptionError):
            EncryptionManager(secret='key1')

        with self.assertRaises(EncryptionError):
            EncryptionManager(secret=b'key1')

    def test_default_correct_secret(self):
        secret = Fernet.generate_key()
        secret2 = Fernet.generate_key()
        manager11 = EncryptionManager(secret=secret, key='key1')
        manager12 = EncryptionManager(secret=secret, key='key1')
        manager21 = EncryptionManager(secret=secret, key='key2')
        manager22 = EncryptionManager(secret=secret2, key='key2')
        manager23 = EncryptionManager(secret=secret2, key='key1')

        value = 'foo'

        value_m11 = manager11.encrypt(value)
        value_m12 = manager12.encrypt(value)
        value_m21 = manager21.encrypt(value)
        value_m22 = manager22.encrypt(value)
        value_m23 = manager23.encrypt(value)

        assert value_m11.startswith('{}key1$'.format(EncryptionManager.MARKER))
        assert value_m12.startswith('{}key1$'.format(EncryptionManager.MARKER))
        assert value_m21.startswith('{}key2$'.format(EncryptionManager.MARKER))
        assert value_m22.startswith('{}key2$'.format(EncryptionManager.MARKER))
        assert value_m23.startswith('{}key1$'.format(EncryptionManager.MARKER))

        assert manager11.decrypt(value_m11) == value
        assert manager11.decrypt(value_m12) == value
        assert manager12.decrypt(value_m12) == value

        with self.assertRaises(EncryptionError):
            manager21.decrypt(value_m12)

        with self.assertRaises(EncryptionError):
            manager22.decrypt(value_m12)

        with self.assertRaises(EncryptionError):
            manager23.decrypt(value_m12)
