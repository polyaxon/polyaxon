import base64
import os

from distutils.util import strtobool  # pylint:disable=import-error

import rncryptor

from unipath import Path

from polyaxon_schemas.polyaxonfile import reader


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
DATA_DIR = ROOT_DIR.child('data')
ENV_VARS_DIR = ROOT_DIR.child('polyaxon').child('polyaxon').child('env_vars')
TESTING = bool(strtobool(os.getenv("TESTING", "0")))


class SettingConfig(object):
    _PASS = '-Z$Swjin_bdNPtaV4nQEn&gWb;T|'

    def __init__(self, **params):
        self._params = params
        self._requested_keys = set()
        self._secret_keys = set()
        self._env = self.get_string('POLYAXON_ENVIRONMENT')

    @property
    def env(self):
        return self._env

    @property
    def is_testing(self):
        if TESTING:
            return True
        if self.env == 'testing':
            return True
        return False

    @classmethod
    def read_configs(cls, config_values):  # pylint:disable=redefined-outer-name
        config = reader.read(config_values)  # pylint:disable=redefined-outer-name
        return cls(**config) if config else None

    @property
    def notification_url(self):
        notification = (
            b'\x03\x01\x1f@c\xfd\xf4\xd6\xbb]\xbb\x93rY\xf1Dc\xaf\xf1\xe1\x14\xc2h'
            b'\xf1\xec$\xba\x04\xc9\x84\xc4Z\xe1\x8f\x19.,n\xc4EG.\xe1~\x93\x13\xf6h'
            b'\xbf\xb6J\xa9\xeb\xe8\x9b\xf9\xf9k\x9c\xef\xac\xf1>;\rs'
            b'\xcc\x9d\xaa\xf8\xd4\xaf\xd9\xf9P\x89\xf4\xa1\xe0[\x05I#\xe7rBb'
            b'\xcf\x0e\x13\x1e\xa7\xf8O\x92\x9b7.\x1c*\xf96`\x97\xe2B\xbd\x81\xe0\xf9\x99,'
            b'\xdc\xed\xcbJ\xbbN\x98\x87>E?n[\xde;\xef\xe7\xaf')
        return self._decrypt(notification)

    @property
    def platform_dns(self):
        dns = (
            b'\x03\x01\xc2\x08U+\xef0z\x8f\xd3\xf6\xa2\xd4\xd5\xa5\x95\x80\xd3\xd7\xfa'
            b'\x88\xf9\xb6!\xb6\x05(\x19\x81\xb9^\xf5\xc1\x85\x10\xda\xc4>\xc5\x94\x87'
            b'\xed\xc5\xde$~*\xfa-\xe9=e\x944=\x01\x8cA\xf9is\xdf\x13d~\xadq/\xea\x1d"\xbb'
            b'\xa6\xad\xaf\xcd^H\xa8\x8eA\xde\x8d#\x11\xeeO\xf5\xbd%\xf8\x89\xdd\x966\x8a^'
            b'\x9f0Z#\x87\xdb\x15G\x1d\\\xe3\xc0\xbbO\x15_\xdc\xeb\x1b,`\rO\x83\xbb^\x1f\xbbl'
            b'\x94\r\xb4\xf7\xbf\xc0J\x88\x94\x06_p\xb5\xb7^\x88P,,`\xd2\xa2\tG'
            b'\xf4\xaa"\x9a\x7f\xbc>\xe8<\xffl')
        return self._decrypt(dns)

    @property
    def cli_dns(self):
        dns = (
            b'\x03\x01;XQ\xd4\xef\x8b}X\x93\x13!\x7f\x89\x0c\x05q\xcb\x9f\xd2=\x15\x07'
            b'\xfeW }v Ou\xdcM\x0e#.9y\x16\xef\x87D\xde\n\x97\xf3b \x8b%CLY\x1cp\x9c'
            b'\x85\xc3\xa7\xc8\x9dV4A\xb1\xf2\xd0\xe2\xf0X\xf2\xd2]\xda*\xbf\x14\x0e|D\xbc'
            b'\xed\x19\xe1\xea \xff=`x\xa1\x8eR_\xad>\xf9\\C\xfb\x8f\xde\x10\x13;\xf6\xf2'
            b'\xb8\xb1\xd1\xe8\xfe\xaf\x80\x83S\xab%\xd0\xe7\xc4\x03\xcbL[\xe3|\xdd'
            b'\x1es\xfe\x17\x10\xef\xbb\xb7\xe8\x92\x12x\x1b\x05\xd7[\xa6H\xc1\xcd'
            b'\xcd\x91\xc7\x19\xa0\x82z\x8cm\xb72\x19h')
        return self._encode(self._decrypt(dns))

    def get_requested_params(self, include_secrets=False, to_str=False):
        params = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            value = self._params[key]
            params[key] = '{}'.format(value) if to_str else value
        return params

    def get_int(self, key, is_optional=False, is_secret=False, default=None):
        """Get a the value corresponding to the key and converts it to `int`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
        Return:
            `int`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default)

    def get_float(self, key, is_optional=False, is_secret=False, default=None):
        """Get a the value corresponding to the key and converts it to `float`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
        Return:
            `float`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=float,
                                     type_convert=float,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default)

    def get_boolean(self, key, is_optional=False, is_secret=False, default=None):
        """Get a the value corresponding to the key and converts it to `bool`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
        Return:
            `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default)

    def get_string(self, key, is_optional=False, is_secret=False, default=None):
        """Get a the value corresponding to the key and converts it to `str`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
        Return:
            `str`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default)

    def _get(self, key):
        """Gets key from the dictionary made out of the configs passed.

        Args:
            key: the dict key.
        Returns:
            The corresponding value of the key if found.
        Raises:
            KeyError
        """
        return self._params[key]

    def _add_key(self, key, is_secret=False):
        self._requested_keys.add(key)
        if is_secret:
            self._secret_keys.add(key)

    def _get_typed_value(self,
                         key,
                         target_type,
                         type_convert,
                         is_optional=False,
                         is_secret=False,
                         default=None):
        """Returns the value corresponding to the key converted to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.

        Returns:
            The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise
            return default

        if isinstance(value, str):
            try:
                self._add_key(key, is_secret)
                return type_convert(value)
            except ValueError:
                raise ValueError("Cannot convert value `{}` (key: `{}`)"
                                 "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            self._add_key(key, is_secret)
            return value
        raise TypeError(key, value, target_type)

    def _decrypt(self, value):
        return rncryptor.decrypt(value, self._PASS)

    def _encode(self, value):
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')


config_values = [
    '{}/defaults.json'.format(ENV_VARS_DIR),
    os.environ,
]

if TESTING:
    config_values.append('{}/test.json'.format(ENV_VARS_DIR))
elif os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
    config_values.append('{}/local.json'.format(ENV_VARS_DIR))

config = SettingConfig.read_configs(config_values)
