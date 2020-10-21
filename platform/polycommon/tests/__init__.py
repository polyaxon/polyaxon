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

try:
    import django

    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
        ROOT_URLCONF="",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
        ],
        SITE_ID=1,
        FIXTURE_DIRS=[""],
        AUDITOR_BACKEND=None,
        AUDITOR_EVENTS_TASK=None,
        WORKERS_BACKEND=None,
        WORKERS_SERVICE=None,
        EXECUTOR_BACKEND=None,
        EXECUTOR_SERVICE=None,
        CONF_BACKEND=None,
        CONF_CHECK_OWNERSHIP=False,
        STORE_OPTION="env",
    )
    django.setup()

except ImportError:
    raise ImportError(
        "To fix this error, run: pip install -r requirements/requirements-test.txt"
    )
