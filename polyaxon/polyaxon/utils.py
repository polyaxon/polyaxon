import os

from distutils.util import strtobool

from unipath import Path

from polyaxon_schemas.polyaxonfile import reader


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
DATA_DIR = ROOT_DIR.child('data')
ENV_VARS_DIR = ROOT_DIR.child('polyaxon').child('polyaxon').child('env_vars')
TESTING = bool(strtobool(os.getenv("TESTING", "0")))


class SettingConfig(object):
    def __init__(self, **params):
        self._params = params
        self._requested_keys = set()
        self._secret_keys = set()

    @classmethod
    def read_configs(cls, config_values):
        config = reader.read(config_values)
        return cls(**config) if config else None

    def get_requested_params(self, include_secrets=False, to_str=False):
        params = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            value = self._params[key]
            params[key] = '{}'.format(value) if to_str else value
        return params

    def get_int(self, key, is_optional=False, is_secret=False):
        """Get a the value corresponding to the key and converts it to `int`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `int`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=lambda x: int(x),
                                     is_optional=is_optional,
                                     is_secret=is_secret)

    def get_float(self, key, is_optional=False, is_secret=False):
        """Get a the value corresponding to the key and converts it to `float`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `float`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=float,
                                     type_convert=lambda x: float(x),
                                     is_optional=is_optional,
                                     is_secret=is_secret)

    def get_boolean(self, key, is_optional=False, is_secret=False):
        """Get a the value corresponding to the key and converts it to `bool`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret)

    def get_string(self, key, is_optional=False, is_secret=False):
        """Get a the value corresponding to the key and converts it to `str`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `str`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=lambda x: str(x),
                                     is_optional=is_optional,
                                     is_secret=is_secret)

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

    def _get_typed_value(self, key, target_type, type_convert, is_optional=False, is_secret=False):
        """Returns the value corresponding to the key converted to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise  an error if key was not found.

        Returns:
            The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise
            return None

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


config_values = [
    '{}/defaults.json'.format(ENV_VARS_DIR),
    os.environ,
]

if TESTING:
    config_values.append('{}/test.json'.format(ENV_VARS_DIR))
elif os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
    config_values.append('{}/local.json'.format(ENV_VARS_DIR))

config = SettingConfig.read_configs(config_values)
