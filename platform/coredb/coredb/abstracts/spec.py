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


class SpecModel(models.Model):
    raw_content = models.TextField(
        null=True,
        blank=True,
        help_text="The raw yaml content of the polyaxonfile/specification.",
    )
    content = models.TextField(
        null=True,
        blank=True,
        help_text="The compiled yaml content of the polyaxonfile/specification.",
    )

    class Meta:
        abstract = True
