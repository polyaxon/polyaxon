# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def remove_empty_keys(config_dict):
    keys = list(config_dict.keys())
    for key in keys:
        if config_dict[key] is None:
            config_dict.pop(key)

    return config_dict
