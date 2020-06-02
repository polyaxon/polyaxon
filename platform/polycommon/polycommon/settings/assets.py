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
from polycommon.config_manager import ConfigManager


def set_assets(context, root_dir, config: ConfigManager):
    context["MEDIA_ROOT"] = config.get_string("POLYAXON_MEDIA_ROOT")
    context["MEDIA_URL"] = config.get_string("POLYAXON_MEDIA_URL")

    context["STATIC_ROOT"] = config.get_string("POLYAXON_STATIC_ROOT")
    context["STATIC_URL"] = config.get_string("POLYAXON_STATIC_URL")

    # Additional locations of static files
    context["STATICFILES_DIRS"] = (str(root_dir.parent.parent / "public"),)

    context["STATICFILES_FINDERS"] = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    context["LOCALE_PATHS"] = (
        str(root_dir / "locale"),
        str(root_dir / "client" / "js" / "libs" / "locale"),
    )

    context["STATICI18N_ROOT"] = "static"
    context["STATICI18N_OUTPUT_DIR"] = "jsi18n"

    context["ARTIFACTS_ROOT"] = config.get_string(
        "POLYAXON_ARTIFACTS_ROOT",
        is_optional=True,
        default="/tmp/plx/artifacts_uploads",
    )
    context["LOGS_ROOT"] = config.get_string(
        "POLYAXON_LOGS_ROOT", is_optional=True, default="/tmp/plx/logs_uploads"
    )
    context["ARCHIVES_ROOT"] = config.get_string(
        "POLYAXON_ARCHIVES_ROOT", is_optional=True, default="/tmp/plx/archives"
    )
