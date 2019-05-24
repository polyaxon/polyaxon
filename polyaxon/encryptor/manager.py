import binascii

from base64 import b64decode, b64encode

from cryptography.fernet import Fernet, InvalidToken

from django.utils.encoding import smart_bytes

from encryptor.execptions import EncryptionError


class EncryptionManager(object):
    MARKER = u'\xef\xbb\xbf'
    DEFAULT_KEY = 'default'

    _marker_length = len(MARKER)

    def __init__(self, secret=None, key=None):
        self.key = key or self.DEFAULT_KEY
        if not secret:
            self.scheme = None
            return

        try:
            self.scheme = Fernet(smart_bytes(secret))
            self.key = key or 'default'
        except (TypeError, ValueError, binascii.Error):
            raise EncryptionError('Encryption scheme value must be bytes')

    def encrypt(self, value):
        if not self.scheme:
            return value
        value = smart_bytes(value)
        return '{}{}${}'.format(
            self.MARKER,
            self.key,
            b64encode(self.scheme.encrypt(value)).decode(),
        )

    def decrypt(self, value):
        # we assume that if encryption is not configured, it was never configured
        if not self.scheme:
            return value
        if not value.startswith(self.MARKER):
            return value
        try:
            enc_method, enc_data = value[self._marker_length:].split('$', 1)
        except (ValueError, IndexError):
            return value
        if not enc_method:
            return value
        if enc_method != self.key:
            raise EncryptionError('Unknown encryption scheme: {}'.format(enc_method))
        try:
            return self.scheme.decrypt(b64decode(enc_data)).decode()
        except InvalidToken as e:
            raise EncryptionError(e)
