#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models

from polyaxon import live_state


class LiveManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(live_state=live_state.STATE_LIVE)


class ArchivedManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(live_state=live_state.STATE_ARCHIVED)


class RestorableManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            live_state__in={live_state.STATE_LIVE, live_state.STATE_ARCHIVED}
        )
