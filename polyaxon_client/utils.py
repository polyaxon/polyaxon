# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from polyaxon_client.logger import logger


def create_polyaxon_tmp():
    base_path = os.path.join('/tmp', '.polyaxon')
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
        except OSError:
            # Except permission denied and potential race conditions
            # in multi-threaded environments.
            logger.warning('Could not create config directory `%s`', base_path)
    return base_path
