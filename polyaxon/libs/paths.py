# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import os
import shutil

logger = logging.getLogger('polyaxon.libs.paths')


def delete_path(path):
    if not os.path.exists(path):
        return
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except OSError:
        logger.warning('Could not delete path `{}`'.format(path))


def create_path(path):
    try:
        os.mkdir(path)
        os.chmod(path, 0o777)
    except FileExistsError:
        pass
    except OSError as e:
        logger.warning('Could not create path `{}`, exception %s', e)
