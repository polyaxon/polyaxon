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

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0003_run_pipeline"),
    ]

    operations = [
        migrations.RemoveField(model_name="project", name="deleted",),
        migrations.RemoveField(model_name="run", name="deleted",),
        migrations.AddField(
            model_name="project",
            name="live_state",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "live"), (0, "archived"), (-1, "deletion_progressing")],
                default=1,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="run",
            name="live_state",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "live"), (0, "archived"), (-1, "deletion_progressing")],
                default=1,
                null=True,
            ),
        ),
    ]
