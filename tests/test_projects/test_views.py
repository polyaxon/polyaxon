from unittest.mock import patch

import pytest

from flaky import flaky
from rest_framework import status

from django.test import override_settings

from api.projects import queries
from api.projects.serializers import BookmarkedProjectSerializer, ProjectDetailSerializer
from constants.experiment_groups import ExperimentGroupLifeCycle
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.bookmarks import Bookmark
from db.models.build_jobs import BuildJob
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.jobs import Job
from db.models.notebooks import NotebookJob
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from factories.factory_build_jobs import BuildJobFactory
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory, ExperimentJobFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory, TensorboardJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest


@pytest.mark.projects_mark
class TestProjectCreateViewV1(BaseViewTest):
    serializer_class = BookmarkedProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.url = '/{}/projects/'.format(API_V1)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        data = {'name': 'new_project'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        assert self.model_class.objects.last().owner.owner == self.auth_client.user

    @override_settings(ALLOW_USER_PROJECTS=False)
    def test_not_allowed_to_create(self):
        data = {'name': 'new_project'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.projects_mark
class TestProjectListViewV1(BaseViewTest):
    serializer_class = BookmarkedProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.user = self.auth_client.user
        self.url = '/{}/{}'.format(API_V1, self.user.username)
        self.objects = [self.factory_class(user=self.user) for _ in range(self.num_objects)]
        # Other user objects
        self.other_object = self.factory_class()
        # One private project
        self.private = self.factory_class(user=self.other_object.user, is_public=False)
        self.url_other = '/{}/{}'.format(API_V1, self.other_object.user)

        self.queryset = self.model_class.objects.filter(user=self.user)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_get_with_bookmarked_objects(self):
        # Other user bookmark
        Bookmark.objects.create(
            user=self.other_object.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.assertEqual(len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]), 0)

        # Authenticated user bookmark
        Bookmark.objects.create(
            user=self.auth_client.user,
            content_object=self.objects[0])

        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert len([1 for obj in resp.data['results'] if obj['bookmarked'] is True]) == 1

    @flaky(max_runs=3)
    def test_get_others(self):
        resp = self.auth_client.get(self.url_other)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 1

        data = resp.data['results']
        assert len(data) == 1
        assert data[0] == self.serializer_class(self.other_object).data

    @flaky(max_runs=3)
    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == self.queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data


@pytest.mark.projects_mark
class TestProjectDetailViewV1(BaseViewTest):
    serializer_class = ProjectDetailSerializer
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/'.format(API_V1, self.object.user.username, self.object.name)
        self.queryset = self.model_class.objects.filter(user=self.object.user)

        # Create related fields
        for _ in range(2):
            ExperimentGroupFactory(project=self.object)

        # Create related fields
        for _ in range(2):
            ExperimentFactory(project=self.object)

        # Other user objects
        self.other_object = self.factory_class()
        self.url_other = '/{}/{}/{}/'.format(API_V1,
                                             self.other_object.user.username,
                                             self.other_object.name)
        # One private project
        self.private = self.factory_class(is_public=False)
        self.url_private = '/{}/{}/{}/'.format(API_V1,
                                               self.private.user.username,
                                               self.private.name)

        self.object_query = queries.projects_details.get(id=self.object.id)
        self.other_object_query = queries.projects_details.get(id=self.other_object.id)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object_query).data
        assert resp.data['num_experiments'] == 2
        assert resp.data['num_experiment_groups'] == 2

        # Get other public project works
        resp = self.auth_client.get(self.url_other)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.other_object_query).data

        # Get other private project does not work
        resp = self.auth_client.get(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_patch(self):
        new_name = 'updated_project_name'
        data = {'name': new_name}
        assert self.object.name != data['name']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.name != self.object.name
        assert new_object.name == new_name
        assert new_object.experiments.count() == 2
        assert new_object.experiment_groups.count() == 2

        # Patch does not work for other project public and private
        resp = self.auth_client.delete(self.url_other)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        resp = self.auth_client.delete(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_delete_does_not_work_for_unauthorized_projects(self):
        # Delete does not work for other project public and private
        resp = self.auth_client.delete(self.url_other)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        resp = self.auth_client.delete(self.url_private)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    @patch('scheduler.tasks.tensorboards.tensorboards_stop.apply_async')
    @patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async')
    @patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async')
    @patch('scheduler.tasks.jobs.jobs_stop.apply_async')
    @patch('scheduler.tasks.experiments.experiments_stop.apply_async')
    @patch('scheduler.tasks.experiment_groups.experiments_group_stop.apply_async')
    def test_delete_archives_and_schedules_deletion(self,
                                                    xp_group_scheduler_mock,
                                                    xp_scheduler_mock,
                                                    job_scheduler_mock,
                                                    build_scheduler_mock,
                                                    notebook_scheduler_mock,
                                                    tensorboard_scheduler_mock):
        for _ in range(2):
            JobFactory(project=self.object)
            BuildJobFactory(project=self.object)
            TensorboardJobFactory(project=self.object)
            NotebookJobFactory(project=self.object)

        self.object.experiment_groups.first().set_status(ExperimentGroupLifeCycle.RUNNING)
        self.object.experiments.first().set_status(ExperimentLifeCycle.RUNNING)
        self.object.jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.build_jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.notebook_jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.tensorboard_jobs.first().set_status(JobLifeCycle.RUNNING)

        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 2
        assert Job.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert NotebookJob.objects.count() == 2
        assert TensorboardJob.objects.count() == 2

        resp = self.auth_client.delete(self.url)
        assert xp_group_scheduler_mock.call_count == 2
        assert xp_scheduler_mock.call_count == 1
        assert job_scheduler_mock.called
        assert build_scheduler_mock.called
        assert notebook_scheduler_mock.called
        assert tensorboard_scheduler_mock.called

        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert Project.all.filter(user=self.object.user).count() == 0
        assert ExperimentGroup.all.count() == 0
        assert Experiment.all.count() == 0
        assert Job.all.count() == 0
        assert BuildJob.all.count() == 0
        assert TensorboardJob.all.count() == 0
        assert NotebookJob.all.count() == 0

    def test_delete_triggers_stopping_of_experiment_groups(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        experiment_group = ExperimentGroup.objects.first()
        # Add running experiment
        experiment = ExperimentFactory(project=experiment_group.project,
                                       experiment_group=experiment_group)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)

        assert Experiment.objects.count() == 3
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as xp_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert xp_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert ExperimentGroup.all.count() == 0
        assert Experiment.all.count() == 0

    def test_delete_triggers_stopping_of_experiments(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        # Add experiment
        experiment = ExperimentFactory(project=self.object)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)

        assert Experiment.objects.count() == 3
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as xp_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert xp_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert Experiment.all.count() == 0

    def test_delete_triggers_stopping_of_jobs(self):
        assert self.queryset.count() == 1
        for _ in range(2):
            job = JobFactory(project=self.object)
            job.set_status(JobLifeCycle.SCHEDULED)
        assert Job.objects.count() == 2

        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as job_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert job_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert Job.all.count() == 0

    def test_delete_triggers_stopping_of_build_jobs(self):
        assert self.queryset.count() == 1
        for _ in range(2):
            job = BuildJobFactory(project=self.object)
            job.set_status(JobLifeCycle.SCHEDULED)
        assert BuildJob.objects.count() == 2
        assert BuildJob.all.count() == 2

        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as job_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert job_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert BuildJob.all.count() == 0

    def test_delete_triggers_stopping_of_plugin_jobs(self):
        assert self.queryset.count() == 1

        notebook_job = NotebookJobFactory(project=self.object)
        notebook_job.set_status(JobLifeCycle.SCHEDULED)

        tensorboard_job = TensorboardJobFactory(project=self.object)
        tensorboard_job.set_status(JobLifeCycle.SCHEDULED)

        assert NotebookJob.objects.count() == 1
        assert TensorboardJob.objects.count() == 1

        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_stop.apply_async') as notebook_mock_stop:
            with patch('scheduler.tasks.tensorboards.'
                       'tensorboards_stop.apply_async') as tensorboard_mock_stop:
                resp = self.auth_client.delete(self.url)

        assert notebook_mock_stop.called
        assert tensorboard_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert TensorboardJob.objects.count() == 0
        assert NotebookJob.objects.count() == 0
        assert TensorboardJob.all.count() == 0
        assert NotebookJob.all.count() == 0

    @patch('scheduler.tasks.tensorboards.tensorboards_stop.apply_async')
    @patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async')
    @patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async')
    @patch('scheduler.tasks.jobs.jobs_stop.apply_async')
    @patch('scheduler.tasks.experiments.experiments_stop.apply_async')
    @patch('scheduler.tasks.experiment_groups.experiments_group_stop.apply_async')
    def test_archive_schedules_deletion(self,
                                        xp_group_scheduler_mock,
                                        xp_scheduler_mock,
                                        job_scheduler_mock,
                                        build_scheduler_mock,
                                        notebook_scheduler_mock,
                                        tensorboard_scheduler_mock):
        for _ in range(2):
            JobFactory(project=self.object)
            BuildJobFactory(project=self.object)
            TensorboardJobFactory(project=self.object)
            NotebookJobFactory(project=self.object)

        self.object.experiment_groups.first().set_status(ExperimentGroupLifeCycle.RUNNING)
        self.object.experiments.first().set_status(ExperimentLifeCycle.RUNNING)
        self.object.jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.build_jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.notebook_jobs.first().set_status(JobLifeCycle.RUNNING)
        self.object.tensorboard_jobs.first().set_status(JobLifeCycle.RUNNING)

        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        assert Experiment.objects.count() == 2
        assert Job.objects.count() == 2
        assert BuildJob.objects.count() == 2
        assert NotebookJob.objects.count() == 2
        assert TensorboardJob.objects.count() == 2

        resp = self.auth_client.post(self.url + 'archive/')
        assert xp_group_scheduler_mock.call_count == 2
        assert xp_scheduler_mock.call_count == 1
        assert job_scheduler_mock.call_count == 1
        assert build_scheduler_mock.call_count == 1
        assert notebook_scheduler_mock.call_count == 1
        assert tensorboard_scheduler_mock.call_count == 1

        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert Project.all.filter(user=self.object.user).count() == 1
        assert ExperimentGroup.objects.count() == 0
        assert ExperimentGroup.all.count() == 2
        assert Experiment.objects.count() == 0
        assert Experiment.all.count() == 2
        assert Job.objects.count() == 0
        assert Job.all.count() == 2
        assert BuildJob.objects.count() == 0
        assert BuildJob.all.count() == 2
        assert TensorboardJob.objects.count() == 0
        assert TensorboardJob.all.count() == 2
        assert NotebookJob.objects.count() == 0
        assert NotebookJob.all.count() == 2

    def test_archive_triggers_stopping_of_experiment_groups(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        experiment_group = ExperimentGroup.objects.first()
        # Add running experiment
        experiment = ExperimentFactory(project=experiment_group.project,
                                       experiment_group=experiment_group)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)

        assert Experiment.objects.count() == 3
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as xp_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert xp_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert ExperimentGroup.objects.count() == 0
        assert ExperimentGroup.all.count() == 2
        assert Experiment.objects.count() == 0
        assert Experiment.all.count() == 3

    def test_archive_triggers_stopping_of_experiments(self):
        assert self.queryset.count() == 1
        assert ExperimentGroup.objects.count() == 2
        # Add experiment
        experiment = ExperimentFactory(project=self.object)
        # Set one experiment to running with one job
        experiment.set_status(ExperimentLifeCycle.SCHEDULED)
        # Add job
        ExperimentJobFactory(experiment=experiment)

        assert Experiment.objects.count() == 3
        with patch('scheduler.tasks.experiments.experiments_stop.apply_async') as xp_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert xp_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert Experiment.objects.count() == 0
        assert Experiment.all.count() == 3

    def test_archive_triggers_stopping_of_jobs(self):
        assert self.queryset.count() == 1
        for _ in range(2):
            job = JobFactory(project=self.object)
            job.set_status(JobLifeCycle.SCHEDULED)
        assert Job.objects.count() == 2

        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as job_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert job_mock_stop.call_count == 2
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert Job.objects.count() == 0
        assert Job.all.count() == 2

    def test_archive_triggers_stopping_of_build_jobs(self):
        assert self.queryset.count() == 1
        for _ in range(2):
            job = BuildJobFactory(project=self.object)
            job.set_status(JobLifeCycle.SCHEDULED)
        assert BuildJob.objects.count() == 2

        with patch('scheduler.tasks.build_jobs.build_jobs_stop.apply_async') as job_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert job_mock_stop.call_count == 2
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert BuildJob.objects.count() == 0
        assert BuildJob.all.count() == 2

    def test_archive_triggers_stopping_of_plugin_jobs(self):
        assert self.queryset.count() == 1

        notebook_job = NotebookJobFactory(project=self.object)
        notebook_job.set_status(JobLifeCycle.SCHEDULED)

        tensorboard_job = TensorboardJobFactory(project=self.object)
        tensorboard_job.set_status(JobLifeCycle.SCHEDULED)

        assert NotebookJob.objects.count() == 1
        assert TensorboardJob.objects.count() == 1

        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_stop.apply_async') as notebook_mock_stop:
            with patch('scheduler.tasks.tensorboards.'
                       'tensorboards_stop.apply_async') as tensorboard_mock_stop:
                resp = self.auth_client.post(self.url + 'archive/')

        assert notebook_mock_stop.call_count == 1
        assert tensorboard_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 0
        assert TensorboardJob.objects.count() == 0
        assert NotebookJob.objects.count() == 0
        assert TensorboardJob.all.count() == 1
        assert NotebookJob.all.count() == 1
