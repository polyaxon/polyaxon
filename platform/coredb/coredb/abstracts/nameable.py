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

from django.core.validators import validate_slug
from django.db import models

from polycommon.validation.blacklist import validate_blacklist_name


class NameableModel(models.Model):
    name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        validators=[validate_slug, validate_blacklist_name],
    )

    class Meta:
        abstract = True


class RequiredNameableModel(models.Model):
    name = models.CharField(
        max_length=128, validators=[validate_slug, validate_blacklist_name]
    )

    class Meta:
        abstract = True
