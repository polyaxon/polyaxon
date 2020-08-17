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

from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_db_model_name(name: str) -> str:
    db = settings.AUTH_USER_MODEL.split(".")[0]
    return "{}.{}".format(db, name)


def get_db_model(name: str) -> str:
    model_name = get_db_model_name(name)
    try:
        return django_apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "{} must be of the form 'app_label.model_name'".format(model_name)
        )
    except LookupError:
        raise ImproperlyConfigured(
            "{} refers to model '{}' that has not been installed".format(
                name, model_name
            )
        )


def get_project_model():
    return get_db_model("Project")


def get_run_model():
    return get_db_model("Run")


def get_artifact_model():
    return get_db_model("Artifact")


def get_lineage_model():
    return get_db_model("ArtifactLineage")
