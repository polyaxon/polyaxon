import base64

from distutils.util import strtobool  # pylint:disable=import-error

from django.utils.functional import cached_property

from config_manager.exceptions import ConfigurationError
from config_manager.uri_spec import UriSpec
from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile import reader


class ConfigManager(object):
    _PASS = '-Z$Swjin_bdNPtaV4nQEn&gWb;T|'

    def __init__(self, **params):
        self._params = params
        self._requested_keys = set()
        self._secret_keys = set()
        self._local_keys = set()

    @classmethod
    def read_configs(cls, config_values):  # pylint:disable=redefined-outer-name
        try:
            config = reader.read(config_values)  # pylint:disable=redefined-outer-name
            return cls(**config) if config else None
        except PolyaxonConfigurationError as e:
            raise ConfigurationError(e)

    @cached_property
    def decode_iterations(self):
        return self.get_int('_POLYAXON_DECODE_ITERATION', is_optional=True, default=1)

    def params_startswith(self, term):
        return [k for k in self._params if k.startswith(term)]

    def params_endswith(self, term):
        return [k for k in self._params if k.endswith(term)]

    def get_requested_params(self, include_secrets=False, include_locals=False, to_str=False):
        params = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            if not include_locals and key in self._local_keys:
                continue
            value = self._params[key]
            params[key] = '{}'.format(value) if to_str else value
        return params

    def get_int(self,
                key,
                is_optional=False,
                is_secret=False,
                is_local=False,
                default=None,
                options=None):
        """Get a the value corresponding to the key and converts it to `int`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `int`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_float(self,
                  key,
                  is_optional=False,
                  is_secret=False,
                  is_local=False,
                  default=None,
                  options=None):
        """Get a the value corresponding to the key and converts it to `float`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `float`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=float,
                                     type_convert=float,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_boolean(self,
                    key,
                    is_optional=False,
                    is_secret=False,
                    is_local=False,
                    default=None,
                    options=None):
        """Get a the value corresponding to the key and converts it to `bool`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_string(self, key,
                   is_optional=False,
                   is_secret=False,
                   is_local=False,
                   default=None,
                   options=None):
        """Get a the value corresponding to the key and converts it to `str`.

        :param key: the dict key.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.
        :return: `str`: value corresponding to the key.
        """
        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def _get(self, key):
        """Gets key from the dictionary made out of the configs passed.

        :param key: the dict key.
        :return: The corresponding value of the key if found.
        :raise: KeyError
        """
        return self._params[key]

    def _add_key(self, key, is_secret=False, is_local=False):
        self._requested_keys.add(key)
        if is_secret:
            self._secret_keys.add(key)
        if is_local:
            self._local_keys.add(key)

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
                         is_local=False,
                         default=None,
                         options=None):
        """Returns the value corresponding to the key converted to the given type.

        :param key: the dict key.
        :param target_type: The type we expect the variable or key to be in.
        :param type_convert: A lambda expression that converts the key to the desired type.
        :param is_optional: To raise an error if key was not found.
        :param is_secret: If the key is a secret.
        :param is_local: If the key is a local to this service.
        :param default: default value if is_optional is True.
        :param options: list/tuple if provided, the value must be one of these values.

        :return: The corresponding value of the key converted.
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
                self._add_key(key, is_secret=is_secret, is_local=is_local)
                self._check_options(key=key, value=value, options=options)
                return type_convert(value)
            except ValueError:
                raise ConfigurationError("Cannot convert value `{}` (key: `{}`)"
                                         "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            self._add_key(key, is_secret=is_secret, is_local=is_local)
            self._check_options(key=key, value=value, options=options)
            return value
        raise ConfigurationError(key, value, target_type)

    def parse_uri_spec(self, uri_spec):
        parts = uri_spec.split('@')
        if len(parts) != 2:
            if self.is_debug_mode:
                raise ConfigurationError(
                    'Received invalid uri_spec `{}`. '
                    'It must be in the format `user:pass@host`'.format(uri_spec))
            else:
                return None

        user_pass, host = parts
        user_pass = user_pass.split(':')
        if len(user_pass) != 2:
            if self.is_debug_mode:
                raise ConfigurationError(
                    'Received invalid uri_spec `{}`. '
                    'It must be in the format `user:pass@host`'.format(uri_spec))
            else:
                return None

        return UriSpec(user=user_pass[0], password=user_pass[1], host=host)

    def _decode(self, value, iteration=3):
        iteration = iteration or self.decode_iterations

        def _decode_once():
            return base64.b64decode(value).decode('utf-8')

        for _ in range(iteration):
            value = _decode_once()
        return value

    @staticmethod
    def _encode(value):
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')
