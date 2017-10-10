# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import ast
import six

from collections import Mapping

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
                " * list: {}}".format(
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
    if isinstance(value, (list, tuple)):
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
TIME_ZONE = timezone('Europe/Berlin')


class TaskType(object):
    MASTER = 'master'
    PS = 'ps'
    WORKER = 'worker'
