import pytest

from mock import patch
from rest_framework.exceptions import ValidationError

from django.test import override_settings

from db.managers.deleted import ArchivedManager, LiveManager
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.projects import Project
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from tests.utils import BaseTest


@pytest.mark.projects_mark
class TestProjectModel(BaseTest):
    def test_has_code(self):
        project = ProjectFactory()
        self.assertEqual(project.has_code, False)

        RepoFactory(project=project)
        self.assertEqual(project.has_code, True)

    def test_has_owner(self):
        project = ProjectFactory()
        self.assertEqual(project.has_owner, True)

    @override_settings(ALLOW_USER_PROJECTS=False)
    def test_cannot_create(self):
        with self.assertRaises(ValidationError):
            ProjectFactory()

    @patch('scheduler.tasks.storage.stores_schedule_logs_deletion.apply_async')
    @patch('scheduler.tasks.storage.stores_schedule_outputs_deletion.apply_async')
    def test_delete_remove_paths(self, delete_outputs_path, delete_logs_path):
        project = ProjectFactory()
        for _ in range(2):
            ExperimentGroupFactory(project=project)
            ExperimentFactory(project=project)
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 2

        with patch('libs.paths.projects.delete_path') as delete_path_project_mock_stop:
            project.delete()
        # 1 repo
        assert delete_path_project_mock_stop.call_count == 1
        # 1 project + 2 * groups + 2 experiments
        assert delete_outputs_path.call_count == 5
        assert delete_logs_path.call_count == 5

    def test_managers(self):
        assert isinstance(Project.objects, LiveManager)
        assert isinstance(Project.archived, ArchivedManager)

    def test_archive(self):
        project = ProjectFactory()
        ExperimentGroupFactory(project=project)
        ExperimentFactory(project=project)
        JobFactory(project=project)
        BuildJobFactory(project=project)
        NotebookJobFactory(project=project)
        TensorboardJobFactory(project=project)

        assert project.deleted is False
        assert project.experiments.count() == 1
        assert project.experiment_groups.count() == 1
        assert project.jobs.count() == 1
        assert project.build_jobs.count() == 1
        assert project.notebook_jobs.count() == 1
        assert project.tensorboard_jobs.count() == 1
        assert project.all_experiments.count() == 1
        assert project.all_experiment_groups.count() == 1
        assert project.all_notebook_jobs.count() == 1
        assert project.all_tensorboard_jobs.count() == 1

        project.archive()
        assert project.deleted is True
        assert project.experiments.count() == 0
        assert project.experiment_groups.count() == 0
        assert project.jobs.count() == 0
        assert project.build_jobs.count() == 0
        assert project.notebook_jobs.count() == 0
        assert project.tensorboard_jobs.count() == 0
        assert project.all_experiments.count() == 1
        assert project.all_experiment_groups.count() == 1
        assert project.all_notebook_jobs.count() == 1
        assert project.all_tensorboard_jobs.count() == 1

        project.restore()
        assert project.deleted is False
        assert project.experiments.count() == 1
        assert project.experiment_groups.count() == 1
        assert project.jobs.count() == 1
        assert project.build_jobs.count() == 1
        assert project.notebook_jobs.count() == 1
        assert project.tensorboard_jobs.count() == 1
        assert project.all_experiments.count() == 1
        assert project.all_experiment_groups.count() == 1
        assert project.all_notebook_jobs.count() == 1
        assert project.all_tensorboard_jobs.count() == 1
