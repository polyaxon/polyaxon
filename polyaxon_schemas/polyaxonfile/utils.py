# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
from collections import Mapping

import six

from polyaxon_schemas.exceptions import PolyaxonConfigurationError
from polyaxon_schemas.polyaxonfile import constants
from polyaxon_schemas.utils import RunTypes


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


def get_vol_path(volume, run_type):
    if run_type == RunTypes.MINIKUBE:
        if volume == constants.LOGS_VOLUME:
            # this is just a hack to allow all pods to write to logs
            return os.path.join('/tmp/plx/', volume)

        # you must run: `minikube mount --v=3 ~/plx/:/plx/`
        # where /plx contains both" /plx/data and /plx/plxfiles
        return os.path.join('/', volume)
    elif run_type == RunTypes.KUBERNETES:
        return os.path.join('/', volume)
    else:
        raise PolyaxonConfigurationError('Run type `{}` is not allowed.'.format(run_type))
