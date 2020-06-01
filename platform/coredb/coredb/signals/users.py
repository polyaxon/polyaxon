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

import uuid

from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from coredb.managers.owners import create_owner, delete_owner
from polyaxon.utils.signal_decorators import ignore_raw, ignore_updates


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_user_owner")
@ignore_updates
@ignore_raw
def create_user_owner(sender, instance=None, created=False, **kwargs):
    create_owner(name=instance.username, uuid=uuid.uuid4())


@receiver(
    post_delete, sender=settings.AUTH_USER_MODEL, dispatch_uid="delete_user_owner"
)
@ignore_raw
def delete_user_owner(sender, instance=None, created=False, **kwargs):
    delete_owner(name=instance.username)
