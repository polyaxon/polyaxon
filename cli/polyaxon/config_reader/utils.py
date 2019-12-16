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


def to_list(value):
    try:
        import numpy as np

        if isinstance(value, np.ndarray):
            return list(value)

    except ImportError:
        pass

    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]
