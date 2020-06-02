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

import uuid

from polyaxon.deploy.operators.cmd_operator import CmdOperator


class ComposeOperator(CmdOperator):
    CMD = "docker-compose"

    @classmethod
    def params(cls, args):
        params = [cls.CMD] + args
        return params

    @classmethod
    def check(cls):
        command_exist = cls.execute(args=["version"])
        if not command_exist:
            return False
        return True

    @classmethod
    def execute(cls, args, stream=False):
        params = cls.params(args)
        return cls._execute(params=params, env=None, stream=stream)

    @staticmethod
    def _generate_worker_env(config):
        # pylint:disable=too-many-branches
        # pylint:disable=too-many-branches
        template = "{}={}"
        env = []
        if not config.worker:
            env.append(template.format("POLYAXON_WORKER_CONCURRENCY", 2))
            return env

        concurrency = config.worker.concurrency or 2
        env.append(template.format("POLYAXON_WORKER_CONCURRENCY", concurrency))
        if config.worker.celery:
            celery = config.worker.celery
            if celery.task_track_started:
                env.append(
                    template.format(
                        "POLYAXON_WORKER_CONCURRENCY", celery.task_track_started
                    )
                )
            if celery.broker_pool_limit:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_BROKER_POOL_LIMIT", celery.broker_pool_limit
                    )
                )
            if celery.confirm_publish:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_CONFIRM_PUBLISH", celery.confirm_publish
                    )
                )
            if celery.worker_prefetch_multiplier:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER",
                        celery.worker_prefetch_multiplier,
                    )
                )
            if celery.worker_max_tasks_per_child:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD",
                        celery.worker_max_tasks_per_child,
                    )
                )
            if celery.worker_max_memory_per_child:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD",
                        celery.worker_max_memory_per_child,
                    )
                )
            if celery.task_always_eager:
                env.append(
                    template.format(
                        "POLYAXON_CELERY_TASK_ALWAYS_EAGER", celery.task_always_eager
                    )
                )
        return env

    @staticmethod
    def _generate_postgres(config):
        template = "{}={}"
        env = []
        if config.postgresql and not config.postgresql.enabled:
            env.append(
                template.format(
                    "POLYAXON_DB_USER", config.external_services.postgresql.user
                )
            )
            env.append(
                template.format(
                    "POLYAXON_DB_PASSWORD", config.external_services.postgresql.password
                )
            )
            env.append(
                template.format(
                    "POLYAXON_DB_NAME", config.external_services.postgresql.database
                )
            )
            env.append(
                template.format(
                    "POLYAXON_DB_HOST", config.external_services.postgresql.host
                )
            )
        return env

    @staticmethod
    def _generate_intervals(config):
        template = "{}={}"
        env = []
        if config.intervals:
            env.append(
                template.format(
                    "POLYAXON_INTERVALS_RUNS_SCHEDULER", config.intervals.runs_scheduler
                )
            )
            env.append(
                template.format(
                    "POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY",
                    config.intervals.operations_default_retry_delay,
                )
            )
            env.append(
                template.format(
                    "POLYAXON_INTERVALS_OPERATIONS_MAX_RETRY_DELAY",
                    config.intervals.operations_max_retry_delay,
                )
            )
        return env

    @staticmethod
    def _generate_email(config):
        template = "{}={}"
        env = []
        if config.email:
            env.append(template.format("POLYAXON_EMAIL_HOST", config.email.host))
            env.append(template.format("POLYAXON_EMAIL_PORT", config.email.port))
            env.append(template.format("POLYAXON_EMAIL_USE_TLS", config.email.use_tls))
            if config.email.host_user:
                env.append(
                    template.format("POLYAXON_EMAIL_HOST_USER", config.email.host_user)
                )
            if config.email.backend:
                env.append(
                    template.format("POLYAXON_EMAIL_BACKEND", config.email.backend)
                )
        return env

    @classmethod
    def generate_env(cls, config):
        # pylint:disable=too-many-statements
        # pylint:disable=too-many-branches
        template = "{}={}"
        env = [template.format("POLYAXON_DEPLOYMENT_TYPE", config.deployment_type)]
        if config.deployment_version:
            env.append(
                template.format("POLYAXON_CHART_VERSION", config.deployment_version)
            )
        if config.namespace:
            env.append(template.format("POLYAXON_K8S_NAMESPACE", config.namespace))
        env.append(
            template.format(
                "POLYAXON_SECRET_KEY", config.polyaxon_secret or uuid.uuid4().hex
            )
        )
        env.append(
            template.format(
                "POLYAXON_SECRET_INTERNAL_TOKEN",
                config.internal_token or uuid.uuid4().hex,
            )
        )
        if config.ssl and config.ssl.enabled and config.ssl.path:
            env.append(template.format("POLYAXON_SSL_ENABLED", config.ssl.enabled))
            env.append(template.format("POLYAXON_SSL_PATH", config.ssl.path))
        env.append(
            template.format(
                "POLYAXON_ADMIN_VIEW_ENABLED", config.admin_view_enabled or False
            )
        )
        if config.timezone:
            env.append(template.format("POLYAXON_TIMEZONE", config.timezone or False))
        env += cls._generate_worker_env(config)
        env += cls._generate_email(config)

        if config.host_name:
            env.append(template.format("POLYAXON_API_HOST", config.host_name))
        if config.allowed_hosts:
            env.append(template.format("POLYAXON_ALLOWED_HOSTS", config.allowed_hosts))

        env += cls._generate_intervals(config)

        if config.log_level:
            env.append(template.format("POLYAXON_LOG_LEVEL", config.log_level))
        env += cls._generate_postgres(config)

        return "\n".join(env)
