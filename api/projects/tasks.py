# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from api.settings import CeleryTasks
from api.celery_api import app

logger = logging.getLogger('polyaxon.api.experiments')


@app.task(name=CeleryTasks.START_EXPERIMENTS)
def start_group_experiments(spec_id):
    pass
