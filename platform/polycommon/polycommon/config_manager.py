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

import os

from pathlib import Path
from typing import List

from polyaxon.config_reader.manager import ConfigManager as BaseConfigManager
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_DEBUG,
    POLYAXON_KEYS_LOG_LEVEL,
    POLYAXON_KEYS_TIME_ZONE,
)
from polyaxon.parser import parser

TESTING = parser.get_boolean(
    "TESTING", os.getenv("TESTING", "0"), is_optional=True, default=False
)


class ConfigManager(BaseConfigManager):
    def __init__(self, **params) -> None:
        super().__init__(**params)
        self._env = self.get_string("POLYAXON_ENVIRONMENT")
        self._service = self.get_string("POLYAXON_SERVICE", is_local=True)
        self._is_debug_mode = self.get_boolean(
            POLYAXON_KEYS_DEBUG, is_optional=True, default=False
        )
        self._namespace = self.get_string("POLYAXON_K8S_NAMESPACE")
        self._log_level = self.get_string(
            POLYAXON_KEYS_LOG_LEVEL, is_local=True, is_optional=True, default="WARNING"
        ).upper()
        self._timezone = self.get_string(
            POLYAXON_KEYS_TIME_ZONE, is_optional=True, default="UTC"
        )
        self._scheduler_enabled = self.get_boolean(
            "POLYAXON_SCHEDULER_ENABLED", is_optional=True, default=False
        )
        self._chart_version = self.get_string(
            "POLYAXON_CHART_VERSION", is_optional=True, default="1.1.8-rc1"
        )
        self._redis_protocol = self.get_string(
            "POLYAXON_REDIS_PROTOCOL", is_optional=True, default="redis"
        )
        self._broker_backend = self.get_string(
            "POLYAXON_BROKER_BACKEND",
            is_optional=True,
            default="rabbitmq",
            options=["redis", "rabbitmq"],
        )
        self._redis_password = self.get_string(
            "POLYAXON_REDIS_PASSWORD", is_optional=True, is_secret=True, is_local=True
        )

    @property
    def namespace(self) -> str:
        return self._namespace

    @property
    def chart_version(self) -> str:
        return self._chart_version

    @property
    def service(self) -> str:
        return self._service

    @property
    def is_monolith_service(self) -> bool:
        return self.service == "monolith"

    @property
    def is_debug_mode(self) -> bool:
        return self._is_debug_mode

    @property
    def env(self) -> str:
        return self._env

    @property
    def is_testing_env(self) -> bool:
        if TESTING:
            return True
        if self.env == "testing":
            return True
        return False

    @property
    def is_local_env(self) -> bool:
        if self.env == "local":
            return True
        return False

    @property
    def is_staging_env(self) -> bool:
        if self.env == "staging":
            return True
        return False

    @property
    def is_production_env(self) -> bool:
        if self.env == "production":
            return True
        return False

    @property
    def log_handlers(self) -> List[str]:
        return ["console"]

    @property
    def log_level(self) -> str:
        if self.is_staging_env or self.is_local_env:
            return self._log_level
        if self._log_level == "DEBUG":
            return "INFO"
        return self._log_level

    @property
    def timezone(self) -> str:
        return self._timezone

    @property
    def scheduler_enabled(self) -> bool:
        return self._scheduler_enabled

    @property
    def broker_backend(self) -> str:
        return self._broker_backend

    @property
    def is_redis_broker(self):
        return self.broker_backend == "redis"

    @property
    def is_rabbitmq_broker(self):
        return self.broker_backend == "rabbitmq"

    def get_redis_url(self, env_url_name) -> str:
        redis_url = self.get_string(env_url_name)
        if self._redis_password:
            redis_url = ":{}@{}".format(self._redis_password, redis_url)
        return "{}://{}".format(self._redis_protocol, redis_url)

    def _get_rabbitmq_broker_url(self) -> str:
        amqp_url = self.get_string("POLYAXON_AMQP_URL")
        rabbitmq_user = self.get_string("POLYAXON_RABBITMQ_USER", is_optional=True)
        rabbitmq_password = self.get_string(
            "POLYAXON_RABBITMQ_PASSWORD",
            is_secret=True,
            is_local=True,
            is_optional=True,
        )
        if rabbitmq_user and rabbitmq_password:
            return "amqp://{user}:{password}@{url}".format(
                user=rabbitmq_user, password=rabbitmq_password, url=amqp_url
            )

        return "amqp://{url}".format(url=amqp_url)

    def get_broker_url(self) -> str:
        if self.broker_backend == "redis":
            return self.get_redis_url("POLYAXON_REDIS_CELERY_BROKER_URL")
        return self._get_rabbitmq_broker_url()


def get_config(context, file_path):
    def base_directory():
        root = Path(os.path.abspath(file_path))
        root.resolve()
        return root.parent.parent.parent

    root_dir = base_directory()
    env_var_dir = root_dir / "polyaxon" / "polyconf" / "env_vars"
    context["ROOT_DIR"] = root_dir
    context["ENV_VARS_DIR"] = env_var_dir

    config_values = [str(env_var_dir / "defaults.json"), os.environ]

    if TESTING:
        config_values.append(str(env_var_dir / "test.json"))
    elif os.path.isfile(str(env_var_dir / "local.json")):
        config_values.append(str(env_var_dir / "local.json"))

    return ConfigManager.read_configs(config_values)
