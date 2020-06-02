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

from django.core.validators import validate_slug
from django.db import models

from coredb.abstracts.projects import BaseProject
from polycommon.validation.blacklist import validate_blacklist_name


class Owner:
    name = "polyaxon"
    uuid = uuid.UUID("9b0a3806e3f84ea1959a7842e34129ed")
    id = 1


class Actor:
    username = "polyaxon"
    id = 1


class Project(BaseProject):
    name = models.CharField(
        max_length=150, unique=True, validators=[validate_slug, validate_blacklist_name]
    )

    class Meta:
        app_label = "coredb"
        db_table = "db_project"
        indexes = [models.Index(fields=["name"])]

    @property
    def owner(self):
        return Owner

    @property
    def owner_id(self):
        return Owner.id

    @property
    def actor(self):
        return Actor
