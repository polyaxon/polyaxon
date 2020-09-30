#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import random

from django.db import models

from coredb.managers.deleted import ArchivedManager, LiveManager
from polycommon import live_state


class LiveStateModel(models.Model):
    live_state = models.IntegerField(
        null=True,
        blank=True,
        default=live_state.STATE_LIVE,
        choices=live_state.CHOICES,
    )

    objects = LiveManager()
    all = models.Manager()
    archived = ArchivedManager()

    class Meta:
        abstract = True

    def delete_in_progress(self) -> bool:
        if self.live_state == live_state.STATE_DELETION_PROGRESSING:
            return False

        self.name = "_{}_d_{}".format(self.name, random.randint(-90, 100))
        self.live_state = live_state.STATE_DELETION_PROGRESSING
        self.save(update_fields=["name", "live_state"])
        return True

    def archive(self) -> bool:
        if (
            self.live_state == live_state.STATE_ARCHIVED
            or self.live_state == live_state.STATE_DELETION_PROGRESSING
        ):
            return False

        self.live_state = live_state.STATE_ARCHIVED
        self.save(update_fields=["live_state"])
        return True

    def restore(self) -> bool:
        if self.live_state != live_state.STATE_ARCHIVED:
            return False

        self.live_state = live_state.STATE_LIVE
        self.save(update_fields=["live_state"])
        return True
