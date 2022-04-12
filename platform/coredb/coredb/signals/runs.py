#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from rest_framework.exceptions import ValidationError

from django.db.models.signals import post_save
from django.dispatch import receiver

from coredb.abstracts.getter import get_run_model
from polyaxon.utils.signal_decorators import ignore_raw, ignore_updates
from polycommon import auditor
from polycommon.events.registry.run import RUN_CREATED


@receiver(post_save, sender=get_run_model(), dispatch_uid="run_created")
@ignore_updates
@ignore_raw
def run_created(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.is_managed:
        if (instance.is_clone and instance.content is None) or (
            not instance.is_clone and instance.raw_content is None
        ):
            raise ValidationError("A managed run should have a valid specification.")
    auditor.record(event_type=RUN_CREATED, instance=instance)
