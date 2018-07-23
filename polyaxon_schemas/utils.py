# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast
import numpy as np
import six

from collections import Mapping
from datetime import datetime
from pytz import timezone

from marshmallow import ValidationError, fields, post_dump, post_load, validate
from marshmallow.base import FieldABC
from marshmallow.utils import _Missing


def get_obj_or_list_obj(container, value, min_length=None, max_length=None):
    try:
        return container.deserialize(value)
    except (ValueError, TypeError, ValidationError):
        pass

    if not isinstance(value, (list, tuple)):
        raise ValidationError("This field expects an int or a list of ints.")

    value = validate.Length(min=min_length, max=max_length)(value)
    try:
        return [container.deserialize(v) for v in value]
    except (ValueError, TypeError):
        raise ValidationError("This field expects an int or a list of ints.")


class UUID(fields.UUID):
    """A UUID field."""

    def _serialize(self, value, attr, obj):
        validated = str(self._validated(value).hex) if value is not None else None
        return super(fields.String, self)._serialize(validated, attr, obj)  # noqa


class IndexedDict(fields.Dict):
    def _validated(self, value):
        """Check the dict has an index or raise a :exc:`ValidationError` if an error occurs."""
        if not (isinstance(value, Mapping) or 'index' in value):
            self.fail('invalid')


class ObjectOrListObject(fields.Field):
    def __init__(self, cls_or_instance, min=None, max=None, **kwargs):  # noqa
        self.min = min
        self.max = max

        super(ObjectOrListObject, self).__init__(**kwargs)
        if isinstance(cls_or_instance, type):
            if not issubclass(cls_or_instance, FieldABC):
                raise ValueError('The type of the list elements '
                                 'must be a subclass of '
                                 'marshmallow.base.FieldABC')
            self.container = cls_or_instance()
        else:
            if not isinstance(cls_or_instance, FieldABC):
                raise ValueError('The instances of the list '
                                 'elements must be of type '
                                 'marshmallow.base.FieldABC')
            self.container = cls_or_instance

    def _deserialize(self, value, attr, data):
        return get_obj_or_list_obj(self.container, value, self.min, self.max)


class Tensor(fields.Field):
    def _deserialize(self, value, attr, data):
        if isinstance(value, six.string_types):
            return [value, 0, 0]
        if isinstance(value, list) and len(value) == 3:
            condition = (isinstance(value[0], str) and
                         isinstance(value[1], int) and
                         isinstance(value[1], int))
            if condition:
                return value
        raise ValidationError("This field expects a str or a list of [str, int, int].")


class PValue(fields.Field):
    def _deserialize(self, value, attr, data):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            if isinstance(value[1], float) and 0 <= value[1] < 1:
                return value
        raise ValidationError("This field expects a list of [value<Any>, dist<float>].")


class IntOrStr(fields.Str):
    default_error_messages = {
        'invalid': 'Not a valid string or int.',
        'invalid_utf8': 'Not a valid utf-8 string.'
    }

    def _serialize(self, value, attr, obj):
        if isinstance(value, int):
            return int(value)

        return super(IntOrStr, self)._serialize(value=value, attr=attr, obj=obj)

    def _deserialize(self, value, attr, data):
        if isinstance(value, int):
            return int(value)

        return super(IntOrStr, self)._deserialize(value=value, attr=attr, data=data)


class Range(fields.Field):
    REQUIRED_KEYS = ['start', 'stop', 'step']
    OPTIONAL_KEY = None
    KEYS = REQUIRED_KEYS

    def _deserialize(self, value, attr, data):
        if isinstance(value, six.string_types):
            value = value.split(':')
        elif isinstance(value, Mapping):
            if set(self.REQUIRED_KEYS) - set(six.iterkeys(value)):
                raise ValidationError("{} dict must have {} keys {}.".format(
                    self.__class__.__name__, len(self.REQUIRED_KEYS), self.REQUIRED_KEYS))
            if len(value) == len(self.REQUIRED_KEYS):
                value = [value[k] for k in self.REQUIRED_KEYS]
            elif len(value) == len(self.KEYS):
                value = [value[k] for k in self.KEYS]
        elif not isinstance(value, list):
            raise ValidationError(
                "{} accept values formatted as the following:\n"
                " * str: {}\n"
                " * dict: {}\n"
                " * list: {}".format(
                    self.__class__.__name__,
                    ':'.join(self.REQUIRED_KEYS),
                    dict(zip(self.REQUIRED_KEYS,
                             ['v{}'.format(i) for i in range(len(self.REQUIRED_KEYS))])),
                    self.REQUIRED_KEYS))

        if len(value) != len(self.REQUIRED_KEYS) and len(value) != len(self.KEYS):
            raise ValidationError("{} requires {} or {} elements received {}".format(
                self.__class__.__name__,
                len(self.REQUIRED_KEYS),
                len(self.KEYS),
                len(value)))

        for i, v in enumerate(value):
            try:
                float(v)
            except (ValueError, TypeError):
                raise ValidationError(
                    "{}: {} must of type int or float, received instead {}".format(
                        self.__class__.__name__, self.REQUIRED_KEYS[i], v
                    ))
            if not isinstance(v, (int, float)):
                value[i] = ast.literal_eval(v)

        # Check that lower value is  smaller than higher value
        if value[0] >= value[1]:
            raise ValidationError(
                "{key2} value must strictly higher that {key1} value, "
                "received instead {key1}: {val1}, {key2}: {val2}".format(
                    key1=self.REQUIRED_KEYS[0],
                    key2=self.REQUIRED_KEYS[1],
                    val1=value[0],
                    val2=value[1]))
        if len(self.REQUIRED_KEYS) == 3 and value[2] == 0:
            raise ValidationError("{} cannot be 0".format(self.REQUIRED_KEYS[2]))

        value = dict(zip(self.KEYS, value))
        return value


class LinSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    KEYS = REQUIRED_KEYS


class GeomSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    KEYS = REQUIRED_KEYS


class LogSpace(Range):
    REQUIRED_KEYS = ['start', 'stop', 'num']
    OPTIONAL_KEYS = ['base']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


def uniform(low, high, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.uniform(low=low, high=high, size=size)


def quniform(low, high, q, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def loguniform(low, high, size=None, rand_generator=None):
    value = uniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.exp(value)


def qloguniform(low, high, q, size=None, rand_generator=None):
    value = loguniform(low=low, high=high, size=size, rand_generator=rand_generator)
    return np.round(value // q) * q


def normal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.normal(loc=loc, scale=scale, size=size)


def qnormal(loc, scale, q, size=None, rand_generator=None):
    draw = normal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.round(draw // q) * q


def lognormal(loc, scale, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    return rand_generator.lognormal(mean=loc, sigma=scale, size=size)


def qlognormal(loc, scale, q, size=None, rand_generator=None):
    draw = lognormal(loc=loc, scale=scale, size=size, rand_generator=rand_generator)
    return np.exp(draw)


def validate_pvalues(values):
    dists = [v for v in values if v]
    if sum(dists) > 1:
        raise ValidationError('The distribution of different outcomes should sum to 1.')


def pvalues(values, size=None, rand_generator=None):
    rand_generator = rand_generator or np.random
    keys = [v[0] for v in values]
    dists = [v[1] for v in values]
    validate_pvalues(dists)
    indices = rand_generator.multinomial(1, dists, size=size)
    if size is None:
        return keys[indices.argmax()]
    return [keys[ind.argmax()] for ind in indices]


class Uniform(Range):
    REQUIRED_KEYS = ['low', 'high']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QUniform(Range):
    REQUIRED_KEYS = ['low', 'high', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogUniform(Range):
    REQUIRED_KEYS = ['low', 'high']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogUniform(Range):
    REQUIRED_KEYS = ['low', 'high', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class Normal(Range):
    REQUIRED_KEYS = ['loc', 'scale']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class LogNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class QLogNormal(Range):
    REQUIRED_KEYS = ['loc', 'scale', 'q']
    OPTIONAL_KEYS = ['size']
    KEYS = REQUIRED_KEYS + OPTIONAL_KEYS


class StrOrFct(fields.Str):
    def serialize(self, attr, obj, accessor=None):
        value = getattr(obj, attr)
        if hasattr(value, '__call__') and hasattr(value, '__name__'):
            return value.__name__

        return super(StrOrFct, self).serialize(attr, obj, accessor)


class DType(fields.Str):
    def serialize(self, attr, obj, accessor=None):
        value = getattr(obj, attr)
        if hasattr(value, 'name'):
            return value.name

        return super(DType, self).serialize(attr, obj, accessor)


class UnknownSchemaMixin(object):
    @post_load(pass_original=True)
    def _handle_load_unknown(self, data, original):
        """Preserve unknown keys during deserialization."""
        for key, val in original.items():
            if key not in self.fields:
                data[key] = val
        return data

    @post_dump(pass_original=True)
    def _handle_dump_unknown(self, data, original):
        """Preserve unknown keys during deserialization."""
        for key, val in original.items():
            if key not in self.fields:
                data[key] = val
        return data


def to_list(value):
    if isinstance(value, (np.ndarray, list, tuple)):
        return list(value)
    return [value]


missing = _Missing()


def get_value(key, obj, default=missing):
    """Helper for pulling a keyed value off various types of objects"""
    if isinstance(key, int):
        return _get_value_for_key(key, obj, default)
    return _get_value_for_keys(key.split('.'), obj, default)


def _get_value_for_keys(keys, obj, default):
    if len(keys) == 1:
        return _get_value_for_key(keys[0], obj, default)
    return _get_value_for_keys(keys[1:], _get_value_for_key(keys[0], obj, default), default)


def _get_value_for_key(key, obj, default):
    try:
        return obj[key]
    except (KeyError, AttributeError, IndexError, TypeError):
        try:
            attr = getattr(obj, key)
            if callable(attr):
                if hasattr(attr, 'get_config') or hasattr(attr, 'SCHEMA'):
                    return attr

                return attr.__name__

            return attr
        except AttributeError:
            return default


def to_camel_case(snake_str):
    split_str = snake_str.split('_')
    if len(split_str) == 1:
        try:
            return snake_str if str.isupper(snake_str[0]) else snake_str.title()
        except TypeError:
            return snake_str if six.text_type.isupper(snake_str[0]) else snake_str.title()
    return "".join(x.title() for x in split_str)


ACTIVATION_VALUES = [
    'softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid',
    'hard_sigmoid', 'linear'
]
TIME_ZONE = timezone('UTC')


class SearchAlgorithms(object):
    GRID = 'grid'
    RANDOM = 'random'
    HYPERBAND = 'hyperband'
    BO = 'bo'  # bayesian optimization

    GRID_VALUES = [GRID, GRID.upper(), GRID.capitalize()]
    RANDOM_VALUES = [RANDOM, RANDOM.upper(), RANDOM.capitalize()]
    HYPERBAND_VALUES = [HYPERBAND, HYPERBAND.upper(), HYPERBAND.capitalize()]
    BO_VALUES = [BO, BO.upper(), BO.capitalize()]

    VALUES = GRID_VALUES + RANDOM_VALUES + HYPERBAND_VALUES + BO_VALUES

    @classmethod
    def is_grid(cls, value):
        return value in cls.GRID_VALUES

    @classmethod
    def is_random(cls, value):
        return value in cls.RANDOM_VALUES

    @classmethod
    def is_hyperband(cls, value):
        return value in cls.HYPERBAND_VALUES

    @classmethod
    def is_bo(cls, value):
        return value in cls.BO_VALUES


class AcquisitionFunctions(object):
    UCB = 'ucb'
    EI = 'ei'
    POI = 'poi'

    UCB_VALUES = [UCB, UCB.upper(), UCB.capitalize()]
    EI_VALUES = [EI, EI.upper(), EI.capitalize()]
    POI_VALUES = [POI, POI.upper(), POI.capitalize()]

    VALUES = UCB_VALUES + EI_VALUES + POI_VALUES

    @classmethod
    def is_ucb(cls, value):
        return value in cls.UCB_VALUES

    @classmethod
    def is_ei(cls, value):
        return value in cls.EI_VALUES

    @classmethod
    def is_poi(cls, value):
        return value in cls.POI_VALUES


class GaussianProcessesKernels(object):
    RBF = 'rbf'
    MATERN = 'matern'

    RBF_VALUES = [RBF, RBF.upper(), RBF.capitalize()]
    MATERN_VALUES = [MATERN, MATERN.upper(), MATERN.capitalize()]

    VALUES = RBF_VALUES + MATERN_VALUES

    @classmethod
    def is_rbf(cls, value):
        return value in cls.RBF_VALUES

    @classmethod
    def is_mattern(cls, value):
        return value in cls.MATERN_VALUES


class Optimization(object):
    MAXIMIZE = 'maximize'
    MINIMIZE = 'minimize'

    MAXIMIZE_VALUES = [MAXIMIZE, MAXIMIZE.upper(), MAXIMIZE.capitalize()]
    MINIMIZE_VALUES = [MINIMIZE, MINIMIZE.upper(), MINIMIZE.capitalize()]

    VALUES = MAXIMIZE_VALUES + MINIMIZE_VALUES

    @classmethod
    def maximize(cls, value):
        return value in cls.MAXIMIZE_VALUES

    @classmethod
    def minimize(cls, value):
        return value in cls.MINIMIZE_VALUES


class ResourceTypes(object):
    INT = 'int'
    FLOAT = 'float'

    INT_VALUES = [INT, INT.upper(), INT.capitalize()]
    FLOAT_VALUES = [FLOAT, FLOAT.upper(), FLOAT.capitalize()]

    VALUES = INT_VALUES + FLOAT_VALUES

    @classmethod
    def is_int(cls, value):
        return value in cls.INT_VALUES

    @classmethod
    def is_float(cls, value):
        return value in cls.FLOAT_VALUES


class EarlyStoppingPolicy(object):
    EXPERIMENT = 'experiment'
    GROUP = 'group'
    ALL = 'all'

    EXPERIMENT_VALUES = [EXPERIMENT, EXPERIMENT.upper(), EXPERIMENT.capitalize()]
    GROUP_VALUES = [GROUP, GROUP.upper(), GROUP.capitalize()]
    ALL_VALUES = [ALL, ALL.upper(), ALL.capitalize()]

    VALUES = EXPERIMENT_VALUES + GROUP_VALUES + ALL_VALUES

    @classmethod
    def stop_experiment(cls, value):
        return value in cls.EXPERIMENT_VALUES

    @classmethod
    def stop_group(cls, value):
        return value in cls.GROUP_VALUES

    @classmethod
    def stop_all(cls, value):
        return value in cls.ALL_VALUES


class TaskType(object):
    MASTER = 'master'
    PS = 'ps'
    WORKER = 'worker'
    SERVER = 'server'
    SCHEDULER = 'scheduler'

    VALUES = [MASTER, PS, WORKER, SERVER, SCHEDULER]


class Frameworks(object):
    TENSORFLOW = 'tensorflow'
    MXNET = 'mxnet'
    HOROVOD = 'horovod'
    PYTORCH = 'pytorch'

    VALUES = [TENSORFLOW, MXNET, HOROVOD, PYTORCH]


def local_now():
    return TIME_ZONE.localize(datetime.utcnow()).replace(microsecond=0)


def humanize_timesince(start_time):
    """Creates a string representation of time since the given `start_time`."""
    if not start_time:
        return start_time

    delta = local_now() - start_time

    # assumption: negative delta values originate from clock
    #             differences on different app server machines
    if delta.total_seconds() < 0:
        return 'a few seconds ago'

    num_years = delta.days // 365
    if num_years > 0:
        return '{} year{} ago'.format(
            *((num_years, 's') if num_years > 1 else (num_years, '')))

    num_weeks = delta.days // 7
    if num_weeks > 0:
        return '{} week{} ago'.format(
            *((num_weeks, 's') if num_weeks > 1 else (num_weeks, '')))

    num_days = delta.days
    if num_days > 0:
        return '{} day{} ago'.format(
            *((num_days, 's') if num_days > 1 else (num_days, '')))

    num_hours = delta.seconds // 3600
    if num_hours > 0:
        return '{} hour{} ago'.format(*((num_hours, 's') if num_hours > 1 else (num_hours, '')))

    num_minutes = delta.seconds // 60
    if num_minutes > 0:
        return '{} minute{} ago'.format(
            *((num_minutes, 's') if num_minutes > 1 else (num_minutes, '')))

    return 'a few seconds ago'


def humanize_timedelta(seconds):
    """Creates a string representation of timedelta."""
    hours, remainder = divmod(seconds, 3600)
    days, hours = divmod(hours, 24)
    minutes, seconds = divmod(remainder, 60)

    if days:
        result = '{}d'.format(days)
        if hours:
            result += ' {}h'.format(hours)
        if minutes:
            result += ' {}m'.format(minutes)
        return result

    if hours:
        result = '{}h'.format(hours)
        if minutes:
            result += ' {}m'.format(minutes)
        return result

    if minutes:
        result = '{}m'.format(minutes)
        if seconds:
            result += ' {}s'.format(seconds)
        return result

    return '{}s'.format(seconds)


def to_percentage(number, rounding=2):
    """Creates a percentage string representation from the given `number`. The
    number is multiplied by 100 before adding a '%' character.

    Raises `ValueError` if `number` cannot be converted to a number.
    """
    number = float(number) * 100
    number_as_int = int(number)
    rounded = round(number, rounding)

    return '{}%'.format(number_as_int if number_as_int == rounded else rounded)


def to_unit_memory(number):
    """Creates a string representation of memory size given `number`."""
    kb = 1024

    number /= kb

    if number < 100:
        return '{} Kb'.format(round(number, 2))

    number /= kb
    if number < 300:
        return '{} Mb'.format(round(number, 2))

    number /= kb

    return '{} Gb'.format(round(number, 2))
