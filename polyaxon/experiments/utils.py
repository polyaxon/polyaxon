# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings


def get_experiment_outputs_path(experiment_name):
    values = experiment_name.split('.')
    if len(values) == 3:
        values.insert(2, 'independents')
    return os.path.join(settings.UPLOAD_ROOT, '/'.join(values))
