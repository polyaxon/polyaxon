# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import MutableMapping, OrderedDict


def dict_to_str(dictionary):
    """Get a `str` representation of a `dict`.

      Args:
        dictionary: The `dict` to be represented as `str`.

      Returns:
        A `str` representing the `dictionary`.
    """
    return ', '.join('%s = %s' % (k, v) for k, v in sorted(dictionary.items()))


def flatten_dict(dict_, parent_key="", sep="."):
    """Flattens a nested dictionary. Namedtuples within the dictionary are converted to dicts.

    Args:
        dict_: The dictionary to flatten.
        parent_key: A prefix to prepend to each key.
        sep: Separator between parent and child keys, a string. For example
          { "a": { "b": 3 } } will become { "a.b": 3 } if the separator is ".".

    Returns:
        A new flattened dictionary.
    """
    items = []
    for key, value in dict_.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, sep=sep).items())
        elif isinstance(value, tuple) and hasattr(value, "_asdict"):
            dict_items = OrderedDict(zip(value._fields, value))
            items.extend(flatten_dict(dict_items, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)
