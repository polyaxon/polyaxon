from distutils.util import strtobool  # pylint:disable=import-error

from polyaxon_schemas.utils import to_list


def to_bool(value):
    if isinstance(value, str):
        value = strtobool(value)

    if value in (False, 0):
        return False

    if value in (True, 1):
        return True

    raise TypeError('The value `{}` cannot be interpreted as boolean'.format(value))


def get_list(values):
    return to_list(values) if values is not None else []
