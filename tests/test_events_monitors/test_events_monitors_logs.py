import logging
import os
import uuid

from unittest.mock import patch

import pytest

from events_handlers.tasks import events_handle_logs_experiment_job, events_handle_logs_job, \
    events_handle_logs_build_job
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from libs.paths.experiments import get_experiment_logs_path
from polyaxon_schemas.utils import TaskType

from libs.paths.jobs import get_job_logs_path
from tests.utils import BaseTest


@pytest.mark.monitors_mark
class BaseTestLogsHandling(BaseTest):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    @staticmethod
    def get_instance():
        pass

    @staticmethod
    def get_params(instance):
        pass

    @staticmethod
    def get_log_path(instance):
        pass

    @staticmethod
    def handle_event(**params):
        pass

    def test_handle_events_job_logs_create_one_handler(self):
        instance = self.get_instance()

        params = self.get_params(instance)
        self.handle_event(**params)

        # Check new log path is created
        log_path = self.get_log_path(instance)
        assert os.path.exists(log_path) is True

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(instance.unique_name)
        assert len(xp_logger.handlers) == 0  # pylint:disable=len-as-condition
        assert self.file_line_count(log_path) == 1  # pylint:disable=len-as-condition

        # Calling again the task should not reuse handler, and create a new line
        self.handle_event(**params)

        # Check the logger has no file handler, and one line created
        xp_logger = logging.getLogger(instance.unique_name)
        assert len(xp_logger.handlers) == 0  # pylint:disable=len-as-condition
        assert self.file_line_count(log_path) == 2


@pytest.mark.monitors_mark
class TestExperimentJobLogsHandling(BaseTestLogsHandling):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    @staticmethod
    def get_instance():
        with patch('scheduler.tasks.experiments.experiments_build.apply_async') as _:  # noqa
            return ExperimentFactory()

    @staticmethod
    def get_params(instance):
        return dict(experiment_name=instance.unique_name,
                    experiment_uuid=instance.uuid.hex,
                    job_uuid=uuid.uuid4().hex,
                    log_line='First test',
                    task_type=TaskType.MASTER,
                    task_idx=0)

    @staticmethod
    def get_log_path(instance):
        return get_experiment_logs_path(instance.unique_name)

    @staticmethod
    def handle_event(**params):
        events_handle_logs_experiment_job(**params)


@pytest.mark.monitors_mark
class TestJobLogsHandling(BaseTestLogsHandling):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    @staticmethod
    def get_instance():
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
            return JobFactory()

    @staticmethod
    def get_params(instance):
        return dict(job_name=instance.unique_name,
                    job_uuid=instance.uuid.hex,
                    log_line='First test')

    @staticmethod
    def get_log_path(instance):
        return get_job_logs_path(instance.unique_name)

    @staticmethod
    def handle_event(**params):
        events_handle_logs_job(**params)


@pytest.mark.monitors_mark
class TestBuildJobLogsHandling(BaseTestLogsHandling):
    @staticmethod
    def file_line_count(filename):
        return len([_ for _ in open(filename)])

    @staticmethod
    def get_instance():
        return BuildJobFactory()

    @staticmethod
    def get_params(instance):
        return dict(job_name=instance.unique_name,
                    job_uuid=instance.uuid.hex,
                    log_line='First test')

    @staticmethod
    def get_log_path(instance):
        return get_job_logs_path(instance.unique_name)

    @staticmethod
    def handle_event(**params):
        events_handle_logs_build_job(**params)


# Prevent base class from running
del BaseTestLogsHandling
