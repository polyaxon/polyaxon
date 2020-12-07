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

import re

import django.core.validators

from django.db import migrations, models

import polycommon.validation.blacklist


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0006_auto_20201020_1705"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="is_approved",
            field=models.BooleanField(
                default=True,
                help_text="If this entity requires approval before it should run.",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="name",
            field=models.CharField(
                max_length=128,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    ),
                    polycommon.validation.blacklist.validate_blacklist_name,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="name",
            field=models.CharField(db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name="run",
            name="name",
            field=models.CharField(
                blank=True,
                default=None,
                max_length=128,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^[-a-zA-Z0-9_]+\\Z"),
                        "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.",
                        "invalid",
                    ),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("created", "created"),
                    ("resuming", "resuming"),
                    ("warning", "warning"),
                    ("unschedulable", "unschedulable"),
                    ("compiled", "compiled"),
                    ("queued", "queued"),
                    ("scheduled", "scheduled"),
                    ("starting", "starting"),
                    ("running", "running"),
                    ("initializing", "initializing"),
                    ("processing", "processing"),
                    ("succeeded", "succeeded"),
                    ("failed", "failed"),
                    ("upstream_failed", "upstream_failed"),
                    ("stopping", "stopping"),
                    ("stopped", "stopped"),
                    ("skipped", "skipped"),
                    ("retrying", "retrying"),
                    ("unknown", "unknown"),
                ],
                db_index=True,
                default="created",
                max_length=16,
                null=True,
            ),
        ),
    ]
