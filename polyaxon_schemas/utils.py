# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast

import six
from datetime import datetime
from collections import Mapping

import numpy as np
from pytz import timezone

from marshmallow import fields, validate, ValidationError, post_dump, post_load
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
        return super(fields.String, self)._serialize(validated, attr, obj)


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
            if (isinstance(value[0], str) and
                    isinstance(value[1], int) and
                    isinstance(value[1], int)):
                return value
        raise ValidationError("This field expects a str or a list of [str, int, int].")


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
                    dict(zip(self.REQUIRED_KEYS, ['v1', 'v2', 'v3'])),
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
            raise ValidationError("{} value must strictly higher that {} value, "
                                  "received instead min: {}, max: {}".format(self.REQUIRED_KEYS[1],
                                                                             self.REQUIRED_KEYS[0],
                                                                             value[0],
                                                                             value[1]))
        if value[2] == 0:
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


class SEARCH_METHODS(object):
    SEQUENTIAL = 'sequential'
    RANDOM = 'random'

    SEQUENTIAL_VALUES = [SEQUENTIAL, SEQUENTIAL.upper(), SEQUENTIAL.capitalize()]
    RANDOM_VALUES = [RANDOM, RANDOM.upper(), RANDOM.capitalize()]

    VALUES = SEQUENTIAL_VALUES + RANDOM_VALUES

    @classmethod
    def is_sequential(cls, value):
        return value in cls.SEQUENTIAL_VALUES

    @classmethod
    def is_random(cls, value):
        return value in cls.RANDOM_VALUES


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


class RunTypes(object):
    LOCAL = 'local'
    MINIKUBE = 'minikube'
    KUBERNETES = 'kubernetes'
    AWS = 'aws'

    VALUES = [LOCAL, MINIKUBE, KUBERNETES, AWS]


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
    Kb = 1024

    number /= Kb

    if number < 100:
        return '{} Kb'.format(round(number, 2))

    number /= Kb
    if number < 300:
        return '{} Mb'.format(round(number, 2))

    number /= Kb

    return '{} Gb'.format(round(number, 2))
