# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch

from factories.factory_plugins import TensorboardJobFactory, NotebookJobFactory
from factories.factory_projects import ProjectFactory
from plugins.models import TensorboardJob, NotebookJob, NotebookJobStatus, TensorboardJobStatus
from spawner.utils.constants import JobLifeCycle

from tests.utils import BaseTest


class TestPluginsModel(BaseTest):
    def test_project_deletion_cascade_to_tensorboard_job(self):
        assert TensorboardJob.objects.count() == 0
        project = ProjectFactory()
        project.tensorboard = TensorboardJobFactory()
        project.save()
        assert TensorboardJob.objects.count() == 1

        with patch('schedulers.tensorboard_scheduler.stop_tensorboard') as _:
            with patch('schedulers.notebook_scheduler.stop_notebook') as _:
                project.delete()
        assert TensorboardJob.objects.count() == 0

    def test_project_deletion_cascade_to_notebook_job(self):
        assert NotebookJob.objects.count() == 0
        project = ProjectFactory()
        project.notebook = NotebookJobFactory()
        project.save()
        assert NotebookJob.objects.count() == 1

        with patch('schedulers.tensorboard_scheduler.stop_tensorboard') as _:
            with patch('schedulers.notebook_scheduler.stop_notebook') as _:
                project.delete()
        assert NotebookJob.objects.count() == 0

    def test_tensorboard_creation_triggers_status_creation(self):
        assert TensorboardJobStatus.objects.count() == 0
        project = ProjectFactory()
        project.tensorboard = TensorboardJobFactory()
        project.save()

        assert TensorboardJobStatus.objects.count() == 1
        assert project.tensorboard.last_status == JobLifeCycle.CREATED

    def test_notebook_creation_triggers_status_creation(self):
        assert NotebookJobStatus.objects.count() == 0
        project = ProjectFactory()
        project.notebook = NotebookJobFactory()
        project.save()

        assert NotebookJobStatus.objects.count() == 1
        assert project.notebook.last_status == JobLifeCycle.CREATED
