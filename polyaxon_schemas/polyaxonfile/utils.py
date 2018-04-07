# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from collections import Mapping


def deep_update(config, override_config):
    for k, v in six.iteritems(override_config):
        if isinstance(v, Mapping):
            k_config = config.get(k, {})
            if isinstance(k_config, Mapping):
                v_config = deep_update(k_config, v)
                config[k] = v_config
            else:
                config[k] = v
        else:
            config[k] = override_config[k]
    return config


class cached_property(object):  # noqa
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
