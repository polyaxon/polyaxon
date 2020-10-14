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

import django.core.serializers.json

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coredb", "0004_auto_20200905_1523"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artifact", name="summary", field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name="artifactlineage",
            name="is_input",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="inputs",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="meta_info",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="outputs",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="params",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="status_conditions",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
