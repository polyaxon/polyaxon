# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os
import shutil

logger = logging.getLogger('polyaxon.libs.outputs')


def delete_outputs(path):
    if not os.path.exists(path):
        return
    try:
        shutil.rmtree(path)
    except OSError:
        logger.warning('Could not delete outputs `{}`'.format(path))
