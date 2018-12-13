# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from hestia.list_utils import to_list

from polyaxon_client.exceptions import PolyaxonClientException


def validate_tags(tags):
    if not tags:
        return None

    if isinstance(tags, six.string_types):
        tags = [tag.strip() for tag in tags.split(',')]

    for tag in to_list(tags):
        if not (tag and isinstance(tag, six.string_types)):
            raise PolyaxonClientException(
                'Received an invalid tag {}. '
                'Please make sure that the tags are list of strings, '
                'or a string containing comma separated values.'.format(tag))
    return tags
