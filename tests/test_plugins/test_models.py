# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from mock import patch

from factories.factory_plugins import TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from plugins.models import TensorboardJob

from tests.utils import BaseTest


class TestPluginsModel(BaseTest):
    def test_project_deletion_cascade_to_tensorboard_job(self):
        assert TensorboardJob.objects.count() == 0
        project = ProjectFactory()
        project.tensorboard = TensorboardJobFactory()
        project.save()
        assert TensorboardJob.objects.count() == 1

        with patch('spawner.scheduler.stop_tensorboard') as _:
            project.delete()
        assert TensorboardJob.objects.count() == 0
