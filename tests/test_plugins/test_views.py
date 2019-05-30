# pylint:disable=too-many-lines
from unittest.mock import patch

import mock
import pytest

from hestia.internal_services import InternalServices
from rest_framework import status

import conf

from api.plugins.serializers import (
    NotebookJobDetailSerializer,
    NotebookJobStatusSerializer,
    ProjectNotebookJobSerializer,
    ProjectTensorboardJobSerializer,
    TensorboardJobDetailSerializer,
    TensorboardJobStatusSerializer
)
from api.utils.views.protected import ProtectedView
from constants.k8s_jobs import NOTEBOOK_JOB_NAME, TENSORBOARD_JOB_NAME
from constants.urls import API_V1
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.notebooks import NotebookJob, NotebookJobStatus
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob, TensorboardJobStatus
from factories.factory_experiment_groups import ExperimentGroupFactory
from factories.factory_experiments import ExperimentFactory
from factories.factory_plugins import (
    NotebookJobFactory,
    NotebookJobStatusFactory,
    TensorboardJobFactory,
    TensorboardJobStatusFactory
)
from factories.factory_projects import ProjectFactory
from factories.factory_repos import RepoFactory
from factories.fixtures import notebook_spec_parsed_content, tensorboard_spec_parsed_content
from lifecycles.jobs import JobLifeCycle
from options.registry.notebooks import NOTEBOOKS_MOUNT_CODE
from scheduler import notebook_scheduler
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from tests.base.views import BaseViewTest


@pytest.mark.plugins_mark
class TestProjectTensorboardStatusListViewV1(BaseViewTest):
    serializer_class = TensorboardJobStatusSerializer
    model_class = TensorboardJobStatus
    factory_class = TensorboardJobStatusFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        self.set_objects()

    def set_objects(self):
        with patch.object(TensorboardJob, 'set_status') as _:  # noqa
            project = ProjectFactory(user=self.auth_client.user)
            self.job = TensorboardJobFactory(project=project)
        self.url = '/{}/{}/{}/tensorboards/{}/statuses/'.format(API_V1,
                                                                project.user.username,
                                                                project.name,
                                                                self.job.id)
        self.objects = [self.factory_class(job=self.job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        resp = self.internal_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.status == JobLifeCycle.CREATED

        data = {'status': JobLifeCycle.RUNNING}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']

        # Create with message and traceback
        data = {'status': JobLifeCycle.FAILED,
                'message': 'message1',
                'traceback': 'traceback1'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 3
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']

        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 4
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']


@pytest.mark.plugins_mark
class TestProjectTensorboardDetailViewV1(BaseViewTest):
    serializer_class = TensorboardJobDetailSerializer
    model_class = TensorboardJob
    factory_class = TensorboardJobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.set_objects()

    def set_objects(self):
        with patch.object(TensorboardJob, 'set_status') as _:  # noqa
            project = ProjectFactory(user=self.auth_client.user)
            self.object = TensorboardJobFactory(project=project)
        self.object.set_status(JobLifeCycle.CREATED)
        self.object.set_status(JobLifeCycle.SCHEDULED)
        self.url = '/{}/{}/{}/tensorboards/{}/'.format(API_V1,
                                                       project.user.username,
                                                       project.name,
                                                       self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        new_description = 'updated_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description

        # Update name
        data = {'name': 'new_name'}
        assert new_object.name is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_archives_deletes_immediately_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.tensorboards.'
                   'tensorboards_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.tensorboards.'
                   'tensorboards_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_archive_schedule_deletion(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.tensorboards.'
                   'tensorboards_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_archive_schedule_archives_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.tensorboards.'
                   'tensorboards_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_restore(self):
        self.object.archive()
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        resp = self.auth_client.post(self.url + 'restore/')
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_spawner_stop(self):
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url + 'stop/')
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestNotebookStatusListViewV1(BaseViewTest):
    serializer_class = NotebookJobStatusSerializer
    model_class = NotebookJobStatus
    factory_class = NotebookJobStatusFactory
    num_objects = 3
    HAS_AUTH = True
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.SIDECAR

    def setUp(self):
        super().setUp()
        self.set_objects()

    def set_objects(self):
        with patch.object(NotebookJob, 'set_status') as _:  # noqa
            project = ProjectFactory(user=self.auth_client.user)
            self.job = NotebookJobFactory(project=project)
        self.url = '/{}/{}/{}/notebooks/{}/statuses/'.format(API_V1,
                                                             project.user.username,
                                                             project.name,
                                                             self.job.id)
        self.objects = [self.factory_class(job=self.job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('created_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        resp = self.internal_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 1
        last_object = self.model_class.objects.last()
        assert last_object.status == JobLifeCycle.CREATED

        data = {'status': JobLifeCycle.RUNNING}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 2
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']

        # Create with message and traceback
        data = {'status': JobLifeCycle.FAILED,
                'message': 'message1',
                'traceback': 'traceback1'}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 3
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']

        resp = self.internal_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == self.num_objects + 4
        last_object = self.model_class.objects.last()
        assert last_object.job == self.job
        assert last_object.status == data['status']
        assert last_object.message == data['message']
        assert last_object.traceback == data['traceback']


@pytest.mark.plugins_mark
class TestProjectNotebookDetailViewV1(BaseViewTest):
    serializer_class = NotebookJobDetailSerializer
    model_class = NotebookJob
    factory_class = NotebookJobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.set_objects()

    def set_objects(self):
        with patch.object(NotebookJob, 'set_status') as _:  # noqa
            project = ProjectFactory(user=self.auth_client.user)
            self.object = NotebookJobFactory(project=project)
        self.object.set_status(JobLifeCycle.CREATED)
        self.object.set_status(JobLifeCycle.SCHEDULED)
        self.url = '/{}/{}/{}/notebooks/{}/'.format(API_V1,
                                                    project.user.username,
                                                    project.name,
                                                    self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        new_description = 'updated_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description

        # Update name
        data = {'name': 'new_name'}
        assert new_object.name is None
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.name == data['name']

    def test_delete_archives_deletes_immediately_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.called
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Deleted
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 0

    def test_delete_archives_and_schedules_deletion(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        # Patched
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_archive_schedule_deletion(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_schedule_deletion.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_archive_schedule_archives_and_schedules_stop(self):
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_stop.apply_async') as spawner_mock_stop:
            resp = self.auth_client.post(self.url + 'archive/')
        assert resp.status_code == status.HTTP_200_OK
        assert spawner_mock_stop.call_count == 1
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1

    def test_restore(self):
        self.object.archive()
        assert self.model_class.objects.count() == 0
        assert self.model_class.all.count() == 1
        resp = self.auth_client.post(self.url + 'restore/')
        assert resp.status_code == status.HTTP_200_OK
        assert self.model_class.objects.count() == 1
        assert self.model_class.all.count() == 1

    def test_spawner_stop(self):
        assert self.queryset.count() == 1
        with patch('scheduler.notebook_scheduler.stop_notebook') as mock_fct:
            resp = self.auth_client.post(self.url + 'stop/')
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestProjectTensorboardListViewV1(BaseViewTest):
    serializer_class = ProjectTensorboardJobSerializer
    model_class = TensorboardJob
    factory_class = TensorboardJobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/tensorboards/'.format(API_V1,
                                                    self.project.user.username,
                                                    self.project.name)
        self.other_url = '/{}/{}/{}/tensorboards/'.format(API_V1,
                                                          self.other_project.user.username,
                                                          self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class(project=self.other_project)
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.queryset = self.queryset.order_by('-updated_at')
        self.other_object = self.factory_class(project=self.other_project)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Test other
        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK

        jobs_count = self.queryset.all().count()
        assert jobs_count == self.num_objects

        # Getting all jobs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == jobs_count

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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '?sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_filter(self):
        # Wrong filter format raises
        resp = self.auth_client.get(self.url + '?query=created_at<2010-01-01')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        resp = self.auth_client.get(self.url + '?query=created_at:<2010-01-01')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:Finished')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:created|running')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_get_filter_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(
            self.url,
            limit,
            '?query=created_at:>=2010-01-01,status:created|running'))
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


@pytest.mark.plugins_mark
class TestProjectNotebookListViewV1(BaseViewTest):
    serializer_class = ProjectNotebookJobSerializer
    model_class = NotebookJob
    factory_class = NotebookJobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/notebooks/'.format(API_V1,
                                                 self.project.user.username,
                                                 self.project.name)
        self.other_url = '/{}/{}/{}/notebooks/'.format(API_V1,
                                                       self.other_project.user.username,
                                                       self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class(project=self.other_project)
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.queryset = self.queryset.order_by('-updated_at')
        self.other_object = self.factory_class(project=self.other_project)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Test other
        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK

        jobs_count = self.queryset.all().count()
        assert jobs_count == self.num_objects

        # Getting all jobs
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == jobs_count

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

    def test_get_order(self):
        resp = self.auth_client.get(self.url + '?sort=created_at,updated_at')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert data == self.serializer_class(self.queryset.order_by('created_at', 'updated_at'),
                                             many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by('created_at', 'updated_at')
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(self.url,
                                                            limit,
                                                            'sort=created_at,updated_at'))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get('next')
        assert next_page is not None
        assert resp.data['count'] == queryset.count()

        data = resp.data['results']
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.auth_client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None

        data = resp.data['results']
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data

    @pytest.mark.filterwarnings('ignore::RuntimeWarning')
    def test_get_filter(self):
        # Wrong filter format raises
        resp = self.auth_client.get(self.url + '?query=created_at<2010-01-01')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        resp = self.auth_client.get(self.url + '?query=created_at:<2010-01-01')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:Finished')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == 0

        resp = self.auth_client.get(self.url +
                                    '?query=created_at:>=2010-01-01,status:created|running')
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    def test_get_filter_pagination(self):
        limit = self.num_objects - 1
        resp = self.auth_client.get("{}?limit={}&{}".format(
            self.url,
            limit,
            '?query=created_at:>=2010-01-01,status:created|running'))
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


@pytest.mark.plugins_mark
class TestStartProjectTensorboardViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/tensorboard/start'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_start(self):
        assert self.queryset.count() == 1
        assert self.object.tensorboard is None
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.clear_cached_properties()
        assert isinstance(self.object.tensorboard, TensorboardJob)

    def test_spawner_start(self):
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.start_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1

    def test_start_with_updated_config(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.clear_cached_properties()
        content = self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()

        # Starting the tensorboard without config should pass
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Check that still using same config
        self.object.clear_cached_properties()
        assert content == self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()
        self.object.save()

        # Starting again the tensorboard with different config
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        self.object.clear_cached_properties()
        # Check that the image was update
        assert content != self.object.tensorboard.content

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK

    def test_start_during_build_process(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        assert start_mock.call_count == 0

    def test_starting_stopping_tensorboard_creating_new_one_create_new_job(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        self.object.tensorboard.set_status(status=JobLifeCycle.STOPPED)
        assert TensorboardJob.objects.count() == 1
        assert TensorboardJobStatus.objects.count() == 2

        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.clear_cached_properties()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        assert TensorboardJob.objects.count() == 2
        assert TensorboardJobStatus.objects.count() == 3


@pytest.mark.plugins_mark
class TestStartExperimentTensorboardViewV1(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(user=self.auth_client.user, project=self.project)
        self.url = '/{}/{}/{}/experiments/{}/tensorboard/start'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)
        self.queryset = self.model_class.objects

    def test_start(self):
        assert self.queryset.count() == 1
        assert self.object.tensorboard is None
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.clear_cached_properties()
        assert isinstance(self.object.tensorboard, TensorboardJob)
        assert self.project.tensorboard is None

    def test_spawner_start(self):
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.start_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        assert self.project.tensorboard is None

    def test_start_with_updated_config(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.refresh_from_db()
        content = self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()

        # Starting the tensorboard without config should pass
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Check that still using same config
        self.object.clear_cached_properties()
        assert content == self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()
        self.object.save()

        # Starting again the tensorboard with different config
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        self.object.clear_cached_properties()
        # Check that the image was update
        assert content != self.object.tensorboard.content

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.project.tensorboard is None

    def test_start_during_build_process(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        assert start_mock.call_count == 0

    def test_starting_stopping_tensorboard_creating_new_one_create_new_job(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        self.object.tensorboard.set_status(status=JobLifeCycle.STOPPED)
        assert TensorboardJob.objects.count() == 1
        assert TensorboardJobStatus.objects.count() == 2

        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.clear_cached_properties()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        assert TensorboardJob.objects.count() == 2
        assert TensorboardJobStatus.objects.count() == 3
        assert self.project.tensorboard is None


@pytest.mark.plugins_mark
class TestStartExperimentGroupTensorboardViewV1(BaseViewTest):
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            self.object = self.factory_class(user=self.auth_client.user, project=self.project)
        self.url = '/{}/{}/{}/groups/{}/tensorboard/start'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)
        self.queryset = self.model_class.objects

    def test_start(self):
        assert self.queryset.count() == 1
        assert self.object.tensorboard is None
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.clear_cached_properties()
        assert isinstance(self.object.tensorboard, TensorboardJob)
        assert self.project.tensorboard is None

    def test_spawner_start(self):
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.start_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        assert self.project.tensorboard is None

    def test_start_with_updated_config(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.clear_cached_properties()
        content = self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()

        # Starting the tensorboard without config should pass
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Check that still using same config
        self.object.clear_cached_properties()
        assert content == self.object.tensorboard.content

        # Simulate stop the tensorboard
        self.object.tensorboard.delete()
        self.object.save()

        # Starting again the tensorboard with different config
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        self.object.clear_cached_properties()
        # Check that the image was update
        assert content != self.object.tensorboard.content

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as mock_fct:
            resp = self.auth_client.post(
                self.url,
                data={'content': tensorboard_spec_parsed_content.raw_data})

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.project.tensorboard is None

    def test_start_during_build_process(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.tensorboard.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        assert start_mock.call_count == 0

    def test_starting_stopping_tensorboard_creating_new_one_create_new_job(self):
        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        self.object.tensorboard.set_status(status=JobLifeCycle.STOPPED)
        assert TensorboardJob.objects.count() == 1
        assert TensorboardJobStatus.objects.count() == 2

        with patch('scheduler.tasks.tensorboards.tensorboards_start.apply_async') as start_mock:
            self.auth_client.post(self.url)
        self.object.clear_cached_properties()
        assert start_mock.call_count == 1
        assert self.object.tensorboard.last_status == JobLifeCycle.CREATED
        assert TensorboardJob.objects.count() == 2
        assert TensorboardJobStatus.objects.count() == 3
        assert self.project.tensorboard is None


@pytest.mark.plugins_mark
class TestStopProjectTensorboardViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/tensorboard/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = TensorboardJob.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.tensorboards.tensorboards_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestStopExperimentTensorboardViewV1(BaseViewTest):
    model_class = Experiment
    factory_class = ExperimentFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(user=self.auth_client.user, project=self.project)
        tensorboard = TensorboardJobFactory(project=self.project, experiment=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/experiments/{}/tensorboard/stop'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)
        self.queryset = TensorboardJob.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.tensorboards.tensorboards_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestStopExperimentGroupTensorboardViewV1(BaseViewTest):
    model_class = ExperimentGroup
    factory_class = ExperimentGroupFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            self.object = self.factory_class(user=self.auth_client.user, project=self.project)
        tensorboard = TensorboardJobFactory(project=self.project, experiment_group=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        self.url = '/{}/{}/{}/groups/{}/tensorboard/stop'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)
        self.queryset = TensorboardJob.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.tensorboards.tensorboards_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tensorboard_scheduler.stop_tensorboard') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class TestStartNotebookViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        self.url = '/{}/{}/{}/notebook/start'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_post_without_config_fails(self):
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_build(self):
        data = {'content': notebook_spec_parsed_content.raw_data}
        assert self.queryset.count() == 1
        assert self.object.notebook is None
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1
        self.object.clear_cached_properties()
        assert isinstance(self.object.notebook, NotebookJob)

    def test_start(self):
        data = {'content': notebook_spec_parsed_content.raw_data}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.'
                   'projects_notebook_build.apply_async') as build_mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert build_mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == 1

    def test_build_with_updated_config(self):
        data = {'content': notebook_spec_parsed_content.raw_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_201_CREATED
        # Start with default config
        self.object.refresh_from_db()
        content = self.object.notebook.content

        # Simulate stop the notebook
        self.object.notebook.delete()

        # Starting the notebook without config should not pass
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url)

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        # Check that still using same config
        self.object.clear_cached_properties()
        assert self.object.notebook is None

        # Starting again the notebook with different config
        notebook_spec_parsed_content.parsed_data['build']['image'] = 'image_v2'
        data['content'] = str(notebook_spec_parsed_content.parsed_data)
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as _:  # noqa
            self.auth_client.post(self.url, data)

        self.object.clear_cached_properties()
        # Check that the image was update
        assert content != self.object.notebook.content

        # Trying to start an already running job returns 200
        # Starting again the tensorboard with different config
        self.object.notebook.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data=data)

        assert mock_fct.call_count == 0
        assert resp.status_code == status.HTTP_200_OK

    def test_start_during_build_process(self):
        data = {'content': notebook_spec_parsed_content.raw_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            resp = self.auth_client.post(self.url, data=data)

        assert resp.status_code == status.HTTP_201_CREATED
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.notebook.last_status == JobLifeCycle.CREATED

        # Check that user cannot start a new job if it's already building
        self.object.notebook.set_status(status=JobLifeCycle.BUILDING)
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            resp = self.auth_client.post(self.url)

        assert resp.status_code == status.HTTP_200_OK
        assert start_mock.call_count == 0

    def test_starting_stopping_notebook_creating_new_one_create_new_job(self):
        data = {'content': notebook_spec_parsed_content.raw_data}
        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            self.auth_client.post(self.url, data=data)

        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        assert self.object.notebook.last_status == JobLifeCycle.CREATED
        self.object.notebook.set_status(status=JobLifeCycle.STOPPED)
        assert NotebookJob.objects.count() == 1
        assert NotebookJobStatus.objects.count() == 2

        with patch('scheduler.tasks.notebooks.projects_notebook_build.apply_async') as start_mock:
            self.auth_client.post(self.url, data=data)
        self.object.refresh_from_db()
        assert start_mock.call_count == 1
        self.object.clear_cached_properties()
        assert self.object.notebook.last_status == JobLifeCycle.CREATED
        assert NotebookJob.objects.count() == 2
        assert NotebookJobStatus.objects.count() == 3


@pytest.mark.plugins_mark
class TestStopNotebookViewV1(BaseViewTest):
    model_class = Project
    factory_class = ProjectFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.object = self.factory_class(user=self.auth_client.user)
        tensorboard = NotebookJobFactory(project=self.object)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        RepoFactory(project=self.object)
        self.url = '/{}/{}/{}/notebook/stop'.format(
            API_V1,
            self.object.user.username,
            self.object.name)
        self.queryset = self.model_class.objects.all()

    def test_stop_serverless(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 0
        assert mock_git_undo.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_stop_code_mount(self):
        conf.set(key=NOTEBOOKS_MOUNT_CODE, value=True)
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 1
        assert mock_git_undo.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_stop_without_committing_serverless(self):
        data = {'commit': False}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 0
        assert mock_git_undo.call_count == 0
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_stop_without_committing_code_mount(self):
        conf.set(key=NOTEBOOKS_MOUNT_CODE, value=True)
        data = {'commit': False}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.notebooks.projects_notebook_stop.apply_async') as mock_fct:
            with patch('libs.repos.git.commit') as mock_git_commit:
                with patch('libs.repos.git.undo') as mock_git_undo:
                    resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert mock_git_commit.call_count == 0
        assert mock_git_undo.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1

    def test_spawner_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.notebook_scheduler.stop_notebook') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.plugins_mark
class BaseTestPluginViewV1(BaseViewTest):
    plugin_app = ''

    @classmethod
    def _get_url(cls, project, path=None):
        url = '/{}/{}/{}'.format(
            cls.plugin_app,
            project.user.username,
            project.name)

        if path:
            url = '{}/{}'.format(url, path)
        return url

    @classmethod
    def _get_service_url(cls, deployment_name):
        return ProjectJobSpawner._get_proxy_url(  # pylint:disable=protected-access
            namespace='polyaxon',
            job_name=cls.plugin_app,
            deployment_name=deployment_name)

    def test_rejects_anonymous_user_and_redirected_to_login_page(self):
        project = ProjectFactory()
        response = self.client.get(self._get_url(project))
        assert response.status_code == 302

    def test_rejects_user_with_no_privileges(self):
        project = ProjectFactory(is_public=False)
        response = self.auth_client.get(self._get_url(project))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_project_with_no_job(self):
        project = ProjectFactory(user=self.auth_client.user)
        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.plugins_mark
class TestTensorboardProjectViewV1(BaseTestPluginViewV1):
    plugin_app = TENSORBOARD_JOB_NAME

    def test_project_requests_tensorboard_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.tensorboard_scheduler.get_tensorboard_url') as mock_fct:
            response = self.auth_client.get(self._get_url(project))

        assert mock_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/'.format(service_url)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        tensorboard = TensorboardJobFactory(project=project)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'tree/'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'static/components/something?v=4.7.0'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


@pytest.mark.plugins_mark
class TestTensorboardExperimentViewV1(BaseTestPluginViewV1):
    plugin_app = TENSORBOARD_JOB_NAME

    @classmethod
    def _get_url(cls, project, experiment, path=None):  # noqa
        url = '/{}/{}/{}/experiments/{}'.format(
            cls.plugin_app,
            project.user.username,
            project.name,
            experiment.id)

        if path:
            url = '{}/{}'.format(url, path)
        return url

    def test_rejects_anonymous_user_and_redirected_to_login_page(self):
        project = ProjectFactory()
        experiment = ExperimentFactory(project=project)
        response = self.client.get(self._get_url(project, experiment))
        assert response.status_code == 302

    def test_rejects_user_with_no_privileges(self):
        project = ProjectFactory(is_public=False)
        experiment = ExperimentFactory(project=project)
        response = self.auth_client.get(self._get_url(project, experiment))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_project_with_no_job(self):
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        response = self.auth_client.get(self._get_url(project, experiment))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_project_requests_tensorboard_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment=experiment)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.tensorboard_scheduler.get_tensorboard_url') as mock_fct:
            response = self.auth_client.get(self._get_url(project, experiment))

        assert mock_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment=experiment)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project, experiment))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/'.format(service_url)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        experiment = ExperimentFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment=experiment)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, experiment, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'tree/'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, experiment, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'static/components/something?v=4.7.0'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


@pytest.mark.plugins_mark
class TestTensorboardExperimentGroupViewV1(BaseTestPluginViewV1):
    plugin_app = TENSORBOARD_JOB_NAME

    @classmethod
    def _get_url(cls, project, group, path=None):  # pylint:disable=arguments-differ
        url = '/{}/{}/{}/groups/{}'.format(
            cls.plugin_app,
            project.user.username,
            project.name,
            group.id)

        if path:
            url = '{}/{}'.format(url, path)
        return url

    def test_rejects_anonymous_user_and_redirected_to_login_page(self):
        project = ProjectFactory()
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        response = self.client.get(self._get_url(project, group))
        assert response.status_code == 302

    def test_rejects_user_with_no_privileges(self):
        project = ProjectFactory(is_public=False)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        response = self.auth_client.get(self._get_url(project, group))
        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_project_with_no_job(self):
        project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        response = self.auth_client.get(self._get_url(project, group))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_project_requests_tensorboard_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment_group=group)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.tensorboard_scheduler.get_tensorboard_url') as mock_fct:
            response = self.auth_client.get(self._get_url(project, group))

        assert mock_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment_group=group)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project, group))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/'.format(service_url)
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.tensorboard_scheduler.TensorboardSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        with patch('scheduler.tasks.experiment_groups.'
                   'experiments_group_create.apply_async') as _:  # noqa
            group = ExperimentGroupFactory(project=project)
        tensorboard = TensorboardJobFactory(project=project, experiment_group=group)
        tensorboard.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = tensorboard.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_tensorboard_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, group, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'tree/'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, group, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}'.format(
            service_url,
            'static/components/something?v=4.7.0'
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


@pytest.mark.plugins_mark
class TestNotebookViewV1(BaseTestPluginViewV1):
    plugin_app = NOTEBOOK_JOB_NAME

    def test_project_requests_notebook_url(self):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        with patch('scheduler.notebook_scheduler.get_notebook_url') as mock_url_fct:
            with patch('scheduler.notebook_scheduler.get_notebook_token') as mock_token_fct:
                response = self.auth_client.get(self._get_url(project))

        assert mock_url_fct.call_count == 1
        assert mock_token_fct.call_count == 1
        assert response.status_code == 200

    @mock.patch('scheduler.notebook_scheduler.NotebookSpawner')
    def test_redirects_to_proxy_protected_url(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = notebook.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_notebook_url.return_value = service_url

        response = self.auth_client.get(self._get_url(project))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}?token={}'.format(
            service_url,
            'tree',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

    @mock.patch('scheduler.notebook_scheduler.NotebookSpawner')
    def test_redirects_to_proxy_protected_url_with_extra_path(self, spawner_mock):
        project = ProjectFactory(user=self.auth_client.user)
        notebook = NotebookJobFactory(project=project)
        notebook.set_status(status=JobLifeCycle.RUNNING)
        deployment_name = notebook.pod_id
        service_url = self._get_service_url(deployment_name=deployment_name)
        mock_instance = spawner_mock.return_value
        mock_instance.get_notebook_url.return_value = service_url

        # To `tree?`
        response = self.auth_client.get(self._get_url(project, 'tree?'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}?token={}'.format(
            service_url,
            'tree',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)

        # To static files
        response = self.auth_client.get(
            self._get_url(project, 'static/components/something?v=4.7.0'))
        assert response.status_code == 200
        self.assertTrue(ProtectedView.NGINX_REDIRECT_HEADER in response)
        proxy_url = '{}/{}&token={}'.format(
            service_url,
            'static/components/something?v=4.7.0',
            notebook_scheduler.get_notebook_token(notebook)
        )
        self.assertEqual(response[ProtectedView.NGINX_REDIRECT_HEADER], proxy_url)


# Prevent this base class from running tests
del BaseTestPluginViewV1
