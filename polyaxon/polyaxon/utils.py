import base64
import os

from distutils.util import strtobool  # pylint:disable=import-error

from unipath import Path

from polyaxon_schemas.polyaxonfile import reader


class ConfigurationError(Exception):
    pass


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
            'aHR0cHM6Ly93d3cuZ29vZ2xlLWFuYWx5d'
            'Gljcy5jb20vY29sbGVjdD92PTEmdGlkPV'
            'VBLTg5NDkzMzMxLTE=')
        return self._decode(notification)

    @property
    def platform_dns(self):
        dns = (
            'aHR0cHM6Ly82YzhhNDU1ZmU4NTA0NzM3ODV'
            'mZGRkYTEyN2IxMTNhYzpjYzFiOWQxNzQ4ZD'
            'I0Mzg5OGNmZjE1ZDIxNjY5NTI2OUBzZW50c'
            'nkuaW8vMTE5NDk2OQ==')
        return self._decode(dns)

    @property
    def cli_dns(self):
        dns = (
            'aHR0cHM6Ly84MTc4MjEwYjY4NDU0OGE1Yjk2'
            'YjgxMzFmYTY0NWM5ZTozY2IwZGI1OTY5NDU0'
            'NjNkYTUzMmUzNmRiZTQ4NjFmNUBzZW50cnku'
            'aW8vMTE5NzQxNg==')
        return dns

    def get_requested_params(self, include_secrets=False, to_str=False):
        params = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            value = self._params[key]
            params[key] = '{}'.format(value) if to_str else value
        return params

    def get_int(self, key, is_optional=False, is_secret=False, default=None, options=None):
        """Get a the value corresponding to the key and converts it to `int`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.
        Return:
            `int`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default,
                                     options=options)

    def get_float(self, key, is_optional=False, is_secret=False, default=None, options=None):
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
                                     default=default,
                                     options=options)

    def get_boolean(self, key, is_optional=False, is_secret=False, default=None, options=None):
        """Get a the value corresponding to the key and converts it to `bool`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.
        Return:
            `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default,
                                     options=options)

    def get_string(self, key, is_optional=False, is_secret=False, default=None, options=None):
        """Get a the value corresponding to the key and converts it to `str`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.
        Return:
            `str`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     default=default,
                                     options=options)

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

    @staticmethod
    def _check_options(key, value, options):
        if options and value not in options:
            raise ConfigurationError(
                'The value `{}` provided for key `{}` '
                'is not one of the possible values.'.format(value, key))

    def _get_typed_value(self,
                         key,
                         target_type,
                         type_convert,
                         is_optional=False,
                         is_secret=False,
                         default=None,
                         options=None):
        """Returns the value corresponding to the key converted to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise  an error if key was not found.
            is_secret: If the key is a secret.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise ConfigurationError(
                    'No value was provided for the non optional key `{}`.'.format(key))
            return default

        if isinstance(value, str):
            try:
                self._add_key(key, is_secret)
                self._check_options(key=key, value=value, options=options)
                return type_convert(value)
            except ValueError:
                raise ConfigurationError("Cannot convert value `{}` (key: `{}`)"
                                         "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            self._add_key(key, is_secret)
            self._check_options(key=key, value=value, options=options)
            return value
        raise ConfigurationError(key, value, target_type)

    @staticmethod
    def _decode(value):
        return base64.b64decode(value).decode('utf-8')

    @staticmethod
    def _encode(value):
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
