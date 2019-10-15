# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from hestia.list_utils import to_list


def validate_tags(tags):
    if not tags:
        return None

    if isinstance(tags, six.string_types):
        tags = [tag.strip() for tag in tags.split(',')]
    tags = to_list(tags)
    tags = [tag for tag in tags if (tag and isinstance(tag, six.string_types))]
    return tags
