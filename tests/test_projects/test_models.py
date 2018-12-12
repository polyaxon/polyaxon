import pytest
from mock import patch

from rest_framework.exceptions import ValidationError

from django.test import override_settings

from db.managers.deleted import LiveManager
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
    DISABLE_RUNNER = True

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

    def test_delete_remove_paths(self):
        project = ProjectFactory()
        [ExperimentGroupFactory(project=project) for _ in range(2)]
        [ExperimentFactory(project=project) for _ in range(2)]
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 2

        with patch('libs.paths.projects.delete_path') as delete_path_project_mock_stop:
            with patch('libs.paths.experiment_groups.delete_path') as delete_path_group_mock_stop:
                with patch('libs.paths.experiments.delete_path') as delete_path_xp_mock_stop:
                    project.delete()
        # 2 * project + 1 repo
        assert delete_path_project_mock_stop.call_count == 3
        # 2 * 2 * groups
        assert delete_path_group_mock_stop.call_count
        assert delete_path_xp_mock_stop.call_count == 4  # 2 * 2  * groups

    def test_managers(self):
        assert isinstance(Project.objects, LiveManager)

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

        project.unarchive()
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
