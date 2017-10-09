# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from experiments.models import Experiment

admin.site.register(Experiment)
