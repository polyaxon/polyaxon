import pytest

from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_projects import ProjectFactory
from libs.unique_urls import (
    get_build_url,
    get_experiment_group_url,
    get_experiment_health_url,
    get_experiment_url,
    get_job_health_url,
    get_job_url,
    get_project_url,
    get_user_project_url,
    get_user_url
)
from tests.utils import BaseTest


@pytest.mark.libs_mark
class TestUniqueUrls(BaseTest):
    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.experiment = ExperimentFactory()
        self.group = ExperimentGroupFactory()
        self.job = JobFactory()
        self.build = BuildJobFactory()

    def test_get_user_url(self):
        self.assertEqual(get_user_url('foo'), '/foo')

    def test_get_project_url(self):
        unique_name = self.project.unique_name
        self.assertEqual(unique_name, '{}.{}'.format(self.project.user.username, self.project.name))
        self.assertEqual(get_project_url(unique_name=unique_name),
                         '/{}'.format(unique_name.replace('.', '/')))

    def test_get_user_project_url(self):
        self.assertEqual(get_user_project_url(username='foo', project_name='bar'), '/foo/bar')

    def test_get_experiment_url(self):
        unique_name = self.experiment.unique_name
        self.assertEqual(unique_name,
                         '{}.{}.{}'.format(self.experiment.project.user.username,
                                           self.experiment.project.name,
                                           self.experiment.id))
        self.assertEqual(get_experiment_url(unique_name=unique_name),
                         '/{}/{}/experiments/{}'.format(self.experiment.project.user.username,
                                                        self.experiment.project.name,
                                                        self.experiment.id))

    def test_get_experiment_health_url(self):
        self.assertEqual(get_experiment_health_url(unique_name=self.experiment.unique_name),
                         '{}/_heartbeat'.format(get_experiment_url(self.experiment.unique_name)))

    def test_get_experiment_group_url(self):
        unique_name = self.group.unique_name
        self.assertEqual(unique_name,
                         '{}.{}.{}'.format(
                             self.group.project.user.username,
                             self.group.project.name,
                             self.group.id))
        self.assertEqual(get_experiment_group_url(unique_name=unique_name),
                         '/{}/{}/groups/{}'.format(
                             self.group.project.user.username,
                             self.group.project.name,
                             self.group.id))

    def test_get_job_url(self):
        unique_name = self.job.unique_name
        self.assertEqual(unique_name,
                         '{}.{}.jobs.{}'.format(
                             self.job.project.user.username,
                             self.job.project.name,
                             self.job.id))
        self.assertEqual(get_job_url(unique_name=unique_name),
                         '/{}/{}/jobs/{}'.format(
                             self.job.project.user.username,
                             self.job.project.name,
                             self.job.id))

    def test_get_job_health_url(self):
        self.assertEqual(
            get_job_health_url(unique_name=self.job.unique_name),
            '{}/_heartbeat'.format(get_job_url(unique_name=self.job.unique_name)))

    def test_get_build_url(self):
        unique_name = self.build.unique_name
        self.assertEqual(unique_name,
                         '{}.{}.builds.{}'.format(
                             self.build.project.user.username,
                             self.build.project.name,
                             self.build.id))
        self.assertEqual(get_build_url(unique_name=unique_name),
                         '/{}/{}/builds/{}'.format(
                             self.build.project.user.username,
                             self.build.project.name,
                             self.build.id))
