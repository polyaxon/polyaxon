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


def migrate_runtime(apps, schema_editor):
    Run = apps.get_model("coredb", "Run")

    runs = []
    for r in Run.objects.all():
        r.runtime = r.meta_info.pop("meta_kind", None)
        runs.append(r)

    Run.objects.bulk_update(runs, ["meta_info", "runtime"])


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0005_auto_20201005_0913"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="runtime",
            field=models.CharField(blank=True, db_index=True, max_length=12, null=True),
        ),
        migrations.RunPython(migrate_runtime),
    ]
