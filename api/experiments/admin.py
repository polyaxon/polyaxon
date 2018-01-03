# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from experiments.models import Experiment, ExperimentStatus, ExperimentJob, ExperimentJobStatus

admin.site.register(Experiment)
admin.site.register(ExperimentStatus)
admin.site.register(ExperimentJob)
admin.site.register(ExperimentJobStatus)
