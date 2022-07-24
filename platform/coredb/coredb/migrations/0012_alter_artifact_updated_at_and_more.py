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

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0011_alter_artifact_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artifact",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="artifactlineage",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="live_state",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "live"), (0, "archived"), (-1, "deletion_progressing")],
                db_index=True,
                default=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="live_state",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "live"), (0, "archived"), (-1, "deletion_progressing")],
                db_index=True,
                default=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
