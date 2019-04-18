import tempfile

import redis

from mock import patch

from django.conf import settings
from django.core.cache import cache
from django.test import TestCase

import activitylogs
import auditor
import executor
import notifier
import tracker

from polyaxon.settings import RedisPools


class BaseTest(TestCase):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True
    DISABLE_AUDITOR = True

    def setUp(self):
        # Force tasks autodiscover
        from scheduler import tasks  # noqa
        from hpsearch.tasks import bo, grid, health, hyperband, random  # noqa
        from pipelines import health, tasks  # noqa
        from crons import tasks  # noqa
        from events_handlers import tasks  # noqa
        from k8s_events_handlers import tasks  # noqa
        from logs_handlers import tasks  # noqa

        # Flushing all redis databases
        redis.StrictRedis(connection_pool=RedisPools.JOB_CONTAINERS).flushall()
        redis.StrictRedis(connection_pool=RedisPools.TO_STREAM).flushall()
        # Mock dirs
        settings.REPOS_MOUNT_PATH = tempfile.mkdtemp()
        settings.UPLOAD_MOUNT_PATH = tempfile.mkdtemp()
        settings.PERSISTENCE_LOGS['mountPath'] = tempfile.mkdtemp()
        settings.PERSISTENCE_OUTPUTS['outputs']['mountPath'] = tempfile.mkdtemp()
        settings.REPOS_ARCHIVE_ROOT = tempfile.mkdtemp()
        settings.OUTPUTS_ARCHIVE_ROOT = tempfile.mkdtemp()
        settings.OUTPUTS_DOWNLOAD_ROOT = tempfile.mkdtemp()
        settings.LOGS_DOWNLOAD_ROOT = tempfile.mkdtemp()
        settings.LOGS_ARCHIVE_ROOT = tempfile.mkdtemp()
        # Flush cache
        cache.clear()
        # Mock celery default sent task
        self.mock_send_task()

        if self.DISABLE_RUNNER:
            self.disable_experiment_groups_runner()
            self.disable_experiments_runner()
            self.plugin_jobs_runner()

        if not self.DISABLE_EXECUTOR or not self.DISABLE_AUDITOR:
            auditor.validate()
            auditor.setup()
        if not self.DISABLE_AUDITOR:
            tracker.validate()
            tracker.setup()
            activitylogs.validate()
            activitylogs.setup()
            notifier.validate()
            notifier.setup()
        if not self.DISABLE_EXECUTOR:
            executor.validate()
            executor.setup()

        return super().setUp()

    def mock_send_task(self):
        from celery import current_app

        def send_task(name, args=(), kwargs=None, **opts):
            kwargs = kwargs or {}
            task = current_app.tasks[name]
            return task.apply_async(args, kwargs, **opts)

        current_app.send_task = send_task

    def disable_experiment_groups_runner(self):
        patcher = patch('scheduler.tasks.experiment_groups.experiments_group_create.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.tasks.experiment_groups.'
                        'experiments_group_stop_experiments.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.tasks.experiment_groups.'
                        'experiments_group_check_finished.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)

    def disable_experiments_runner(self):
        patcher = patch('scheduler.tasks.experiments.experiments_build.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.experiment_scheduler.stop_experiment')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.tasks.experiments.experiments_stop.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)

    def plugin_jobs_runner(self):
        patcher = patch('scheduler.tensorboard_scheduler.stop_tensorboard')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.notebook_scheduler.stop_notebook')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.dockerizer_scheduler.create_build_job')
        patcher.start()
        self.addCleanup(patcher.stop)

        patcher = patch('scheduler.tasks.jobs.jobs_build.apply_async')
        patcher.start()
        self.addCleanup(patcher.stop)
