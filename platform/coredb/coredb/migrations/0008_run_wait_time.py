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


def migrate_wait_time(apps, schema_editor):
    Run = apps.get_model("coredb", "Run")

    runs = []
    for r in Run.objects.annotate(
        calc_wait_time=models.F("started_at") - models.F("created_at")
    ):
        if r.calc_wait_time:
            r.wait_time = r.calc_wait_time.seconds
            runs.append(r)

    Run.objects.bulk_update(runs, ["wait_time"])


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0007_auto_20201121_1332"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="wait_time",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(migrate_wait_time),
    ]
