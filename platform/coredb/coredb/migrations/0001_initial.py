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
import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
import django.core.validators
import django.db.models.deletion
import django.utils.timezone

from django.conf import settings
from django.db import migrations, models

import polycommon.validation.blacklist


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=30, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "db_table": "db_user",
                "abstract": False,
                "swappable": "AUTH_USER_MODEL",
            },
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Artifact",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("state", models.UUIDField()),
                ("name", models.CharField(db_index=True, max_length=64)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("model", "model"),
                            ("audio", "audio"),
                            ("video", "video"),
                            ("histogram", "histogram"),
                            ("image", "image"),
                            ("tensor", "tensor"),
                            ("dataframe", "dataframe"),
                            ("chart", "chart"),
                            ("csv", "csv"),
                            ("tsv", "tsv"),
                            ("psv", "psv"),
                            ("ssv", "ssv"),
                            ("metric", "metric"),
                            ("env", "env"),
                            ("html", "html"),
                            ("text", "text"),
                            ("file", "file"),
                            ("dir", "dir"),
                            ("tensorboard", "tensorboard"),
                            ("dockerfile", "dockerfile"),
                            ("docker_image", "docker_image"),
                            ("data", "data"),
                            ("coderef", "coderef"),
                            ("table", "table"),
                            ("curve", "curve"),
                        ],
                        db_index=True,
                        max_length=12,
                    ),
                ),
                ("path", models.CharField(blank=True, max_length=256, null=True)),
                ("summary", django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={"db_table": "db_artifact",},
        ),
        migrations.CreateModel(
            name="ArtifactLineage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_input", models.NullBooleanField(default=False)),
            ],
            options={"db_table": "db_artifactlineage",},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                ("readme", models.TextField(blank=True, null=True)),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150,
                        unique=True,
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
            ],
            options={"db_table": "db_project",},
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "name",
                    models.CharField(
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
                            polycommon.validation.blacklist.validate_blacklist_name,
                        ],
                    ),
                ),
                ("readme", models.TextField(blank=True, null=True)),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "is_managed",
                    models.BooleanField(
                        default=True,
                        help_text="If this entity is managed by the platform.",
                    ),
                ),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("run_time", models.IntegerField(blank=True, null=True)),
                (
                    "raw_content",
                    models.TextField(
                        blank=True,
                        help_text="The raw yaml content of the polyaxonfile/specification.",
                        null=True,
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True,
                        help_text="The compiled yaml content of the polyaxonfile/specification.",
                        null=True,
                    ),
                ),
                (
                    "status",
                    models.CharField(
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
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "status_conditions",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        null=True,
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("job", "job"),
                            ("service", "service"),
                            ("dag", "dag"),
                            ("matrix", "matrix"),
                            ("spark", "spark"),
                            ("dask", "dask"),
                            ("flink", "flink"),
                            ("ray", "ray"),
                            ("mpijob", "mpijob"),
                            ("tfjob", "tfjob"),
                            ("pytorchjob", "pytorchjob"),
                            ("scheduler", "scheduler"),
                            ("tuner", "tuner"),
                            ("watchdog", "watchdog"),
                            ("notifier", "notifier"),
                        ],
                        db_index=True,
                        max_length=12,
                    ),
                ),
                (
                    "meta_info",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, default=dict, null=True
                    ),
                ),
                (
                    "params",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                (
                    "inputs",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                (
                    "outputs",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                (
                    "cloning_kind",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("copy", "copy"),
                            ("restart", "restart"),
                            ("cache", "cache"),
                            ("schedule", "schedule"),
                        ],
                        max_length=12,
                        null=True,
                    ),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        blank=True,
                        related_name="runs",
                        through="coredb.ArtifactLineage",
                        to="coredb.Artifact",
                    ),
                ),
                (
                    "original",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="clones",
                        to="coredb.Run",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="runs",
                        to="coredb.Project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "db_run",},
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(fields=["name"], name="db_project_name_4bfc0e_idx"),
        ),
        migrations.AddField(
            model_name="artifactlineage",
            name="artifact",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs_lineage",
                to="coredb.Artifact",
            ),
        ),
        migrations.AddField(
            model_name="artifactlineage",
            name="run",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="artifacts_lineage",
                to="coredb.Run",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="artifact", unique_together={("name", "state")},
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddIndex(
            model_name="run",
            index=models.Index(fields=["name"], name="db_run_name_47fc7c_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="artifactlineage", unique_together={("run", "artifact", "is_input")},
        ),
    ]
