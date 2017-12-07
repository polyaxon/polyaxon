# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from repos.models import Repo, ExternalRepo

admin.site.register(Repo)
admin.site.register(ExternalRepo)
