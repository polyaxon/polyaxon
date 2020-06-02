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
from typing import Dict

from polycommon.config_manager import ConfigManager


def set_celery(context, config: ConfigManager, routes: Dict):
    context["CELERY_TASK_TRACK_STARTED"] = config.get_boolean(
        "POLYAXON_CELERY_TASK_TRACK_STARTED", is_optional=True, default=True
    )

    context["CELERY_BROKER_POOL_LIMIT"] = config.get_int(
        "POLYAXON_CELERY_BROKER_POOL_LIMIT", is_optional=True, default=100
    )

    context["CELERY_BROKER_BACKEND"] = config.broker_backend
    confirm_publish = config.get_boolean(
        "POLYAXON_CELERY_CONFIRM_PUBLISH", is_optional=True, default=True
    )
    context["CELERY_CONFIRM_PUBLISH"] = confirm_publish
    if config.is_rabbitmq_broker and confirm_publish:
        # see https://github.com/celery/celery/issues/5410 for details
        context["CELERY_BROKER_TRANSPORT_OPTIONS"] = {"confirm_publish": True}

    context["CELERY_BROKER_URL"] = config.get_broker_url()

    context["INTERNAL_EXCHANGE"] = config.get_string(
        "POLYAXON_INTERNAL_EXCHANGE", is_optional=True, default="internal"
    )

    context["CELERY_RESULT_BACKEND"] = config.get_redis_url(
        "POLYAXON_REDIS_CELERY_RESULT_BACKEND_URL"
    )

    context["CELERY_WORKER_PREFETCH_MULTIPLIER"] = config.get_int(
        "POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER", is_optional=True, default=4
    )

    eager_mode = config.get_boolean("POLYAXON_CELERY_TASK_ALWAYS_EAGER")
    context["CELERY_TASK_ALWAYS_EAGER"] = eager_mode
    if eager_mode:
        context["CELERY_BROKER_TRANSPORT"] = "memory"

    context["CELERY_ACCEPT_CONTENT"] = ["application/json"]
    context["CELERY_TASK_SERIALIZER"] = "json"
    context["CELERY_RESULT_SERIALIZER"] = "json"
    context["CELERY_TASK_IGNORE_RESULT"] = True
    context["CELERY_TIMEZONE"] = config.timezone
    context["CELERY_HARD_TIME_LIMIT_DELAY"] = config.get_int(
        "POLYAXON_CELERY_HARD_TIME_LIMIT_DELAY", is_optional=True, default=180
    )

    context["CELERY_WORKER_MAX_TASKS_PER_CHILD"] = config.get_int(
        "POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD", is_optional=True, default=100
    )

    context["CELERY_WORKER_MAX_MEMORY_PER_CHILD"] = config.get_int(
        "POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD", is_optional=True, default=400000
    )

    class Intervals:
        """All intervals are in seconds"""

        OPERATIONS_DEFAULT_RETRY_DELAY = config.get_int(
            "POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY",
            is_optional=True,
            default=60,
        )
        OPERATIONS_MAX_RETRY_DELAY = config.get_int(
            "POLYAXON_INTERVALS_OPERATIONS_MAX_RETRY_DELAY",
            is_optional=True,
            default=60 * 60,
        )
        RUNS_SCHEDULER = config.get_int(
            "POLYAXON_INTERVALS_RUNS_SCHEDULER", is_optional=True, default=30
        )

    context["Intervals"] = Intervals
    context["CELERY_TASK_ROUTES"] = routes
