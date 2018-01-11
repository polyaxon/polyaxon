# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from polyaxon.utils import config

# dirs
DIRS_DOCKER = config.get_string('POLYAXON_DIRS_DOCKER')
DIRS_NVIDIA = config.get_string('POLYAXON_DIRS_NVIDIA')
MOUNT_PATHS_NVIDIA = config.get_string('POLYAXON_MOUNT_PATHS_NVIDIA')

if DIRS_NVIDIA:
    DIRS_NVIDIA = json.loads(DIRS_NVIDIA)

if MOUNT_PATHS_NVIDIA:
    MOUNT_PATHS_NVIDIA = json.loads(MOUNT_PATHS_NVIDIA)

    if 'bin' in MOUNT_PATHS_NVIDIA:
        # Update PATH with the nvidia bin
        os.environ['PATH'] = '{}:{}'.format(os.getenv('PATH', ''), MOUNT_PATHS_NVIDIA['bin'])
