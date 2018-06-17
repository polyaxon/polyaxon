# pylint:disable=too-many-lines
from faker import Faker
from unittest.mock import patch

import pytest

from rest_framework import status

from api.jobs.serializers import JobDetailSerializer, JobSerializer, JobStatusSerializer
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from db.models.jobs import Job, JobStatus
from factories.factory_jobs import JobFactory, JobStatusFactory
from factories.factory_projects import ProjectFactory
from factories.fixtures import job_spec_parsed_content
from libs.paths.jobs import create_job_logs_path, get_job_logs_path
from polyaxon_schemas.polyaxonfile.specification import JobSpecification
from tests.utils import BaseViewTest


@pytest.mark.jobs_mark
class TestProjectJobListViewV1(BaseViewTest):
    serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory
    num_objects = 3
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/{}/{}/jobs/'.format(API_V1,
                                            self.project.user.username,
                                            self.project.name)
        self.other_url = '/{}/{}/{}/jobs/'.format(API_V1,
                                                  self.other_project.user.username,
                                                  self.other_project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        # one object that does not belong to the filter
        self.factory_class()
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.other_object = self.factory_class(project=self.other_project)
        self.queryset = self.queryset.order_by('-updated_at')

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

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': job_spec_parsed_content.parsed_data}
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_create_with_runner(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'config': job_spec_parsed_content.parsed_data}
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.jobs_mark
class TestJobListViewV1(BaseViewTest):
    serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.url = '/{}/{}/{}/jobs/'.format(API_V1,
                                            self.project.user,
                                            self.project.name)
        self.objects = [self.factory_class(project=self.project) for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
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


@pytest.mark.jobs_mark
class TestJobDetailViewV1(BaseViewTest):
    serializer_class = JobDetailSerializer
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/'.format(API_V1,
                                               project.user.username,
                                               project.name,
                                               self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        self.object.refresh_from_db()
        assert resp.data == self.serializer_class(self.object).data

    def test_get_with_resource_reg_90(self):
        spec_content = """---
            version: 1

            kind: job

            environment:
              resources:
                gpu:
                  requests: 1
                  limits: 1

            build:
              image: my_image

            run:
              cmd: do_something
        """
        spec_parsed_content = JobSpecification.read(spec_content)

        project = ProjectFactory(user=self.auth_client.user)
        exp = self.factory_class(project=project, config=spec_parsed_content.parsed_data)
        url = '/{}/{}/{}/jobs/{}/'.format(API_V1,
                                          project.user.username,
                                          project.name,
                                          exp.id)

        resp = self.auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        exp.refresh_from_db()
        assert resp.data == self.serializer_class(exp).data

    def test_patch(self):
        new_description = 'updated_xp_name'
        data = {'description': new_description}
        assert self.object.description != data['description']
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description != self.object.description
        assert new_object.description == new_description

        # Update original job
        assert new_object.is_clone is False
        new_job = JobFactory()
        data = {'original_job': new_job.id}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.user == self.object.user
        assert new_object.description == new_description
        assert new_object.is_clone is True
        assert new_object.original_job == new_job

    def test_delete(self):
        self.object.set_status(JobLifeCycle.SCHEDULED)
        assert self.model_class.objects.count() == 1
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as spawner_mock_stop:
            with patch('libs.paths.jobs.delete_path') as outputs_mock_stop:
                resp = self.auth_client.delete(self.url)
        assert spawner_mock_stop.call_count == 1
        assert outputs_mock_stop.call_count == 2  # Outputs and Logs
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 0


@pytest.mark.jobs_mark
class TestJobStatusListViewV1(BaseViewTest):
    serializer_class = JobStatusSerializer
    model_class = JobStatus
    factory_class = JobStatusFactory
    num_objects = 3
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Job, 'set_status') as _:
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                project = ProjectFactory(user=self.auth_client.user)
                self.job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/statuses/'.format(API_V1,
                                                        project.user.username,
                                                        project.name,
                                                        self.job.id)
        self.objects = [self.factory_class(job=self.job,
                                           status=JobLifeCycle.CHOICES[i][0])
                        for i in range(self.num_objects)]
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
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


@pytest.mark.jobs_mark
class TestJobStatusDetailViewV1(BaseViewTest):
    serializer_class = JobStatusSerializer
    model_class = JobStatus
    factory_class = JobStatusFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        with patch.object(Job, 'set_status') as _:  # noqa
            with patch('scheduler.tasks.jobs.jobs_build.apply_async') as _:  # noqa
                self.job = JobFactory()
        self.object = self.factory_class(job=self.job)
        self.url = '/{}/{}/{}/jobs/{}/statuses/{}/'.format(
            API_V1,
            self.job.project.user.username,
            self.job.project.name,
            self.job.id,
            self.object.uuid.hex)
        self.queryset = self.model_class.objects.all()

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

    def test_patch(self):
        data = {'status': JobLifeCycle.SUCCEEDED}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete(self):
        assert self.model_class.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert self.model_class.objects.count() == 1


@pytest.mark.jobs_mark
class TestRestartJobViewV1(BaseViewTest):
    serializer_class = JobSerializer
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/restart'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_restart(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2

        last_job = self.queryset.last()
        assert last_job.is_clone is True
        assert last_job.is_restart is True
        assert last_job.is_copy is False
        assert last_job.is_resume is False
        assert last_job.original_job == self.object
        assert last_job.original_unique_name == self.object.unique_name

    def test_restart_patch_config(self):
        data = {
            'config': {
                'environment': {
                    'resources': {
                        'cpu': {'limits': 0.1, 'requests': 0.2}
                    }
                }
            }
        }
        assert self.queryset.first().specification.environment is None
        with patch('scheduler.tasks.jobs.jobs_build.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert mock_fct.call_count == 1
        assert self.queryset.count() == 2
        assert self.queryset.first().specification.environment is None
        resources = self.queryset.last().specification.environment.resources.to_light_dict()
        assert resources['cpu'] == data['config']['environment']['resources']['cpu']

        last_job = self.queryset.last()
        assert last_job.is_clone is True
        assert last_job.is_restart is True
        assert last_job.is_copy is False
        assert last_job.is_resume is False
        assert last_job.original_job == self.object
        assert last_job.original_unique_name == self.object.unique_name

    def test_restart_patch_wrong_config_raises(self):
        data = {'config': {'lr': 0.1}}
        assert self.queryset.first().specification is not None
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert self.queryset.count() == 1


@pytest.mark.jobs_mark
class TestStopJobViewV1(BaseViewTest):
    model_class = Job
    factory_class = JobFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=project)
        self.url = '/{}/{}/{}/jobs/{}/stop'.format(
            API_V1,
            project.user.username,
            project.name,
            self.object.id)
        self.queryset = self.model_class.objects.all()

    def test_stop(self):
        data = {}
        assert self.queryset.count() == 1
        with patch('scheduler.tasks.jobs.jobs_stop.apply_async') as mock_fct:
            resp = self.auth_client.post(self.url, data)
        assert mock_fct.call_count == 1
        assert resp.status_code == status.HTTP_200_OK
        assert self.queryset.count() == 1


@pytest.mark.jobs_mark
class TestJobLogsViewV1(BaseViewTest):
    num_log_lines = 10
    HAS_AUTH = True
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        project = ProjectFactory(user=self.auth_client.user)
        job = JobFactory(project=project)
        self.url = '/{}/{}/{}/jobs/{}/logs'.format(
            API_V1,
            project.user.username,
            project.name,
            job.id)

        log_path = get_job_logs_path(job.unique_name)
        create_job_logs_path(job_name=job.unique_name)
        fake = Faker()
        self.logs = []
        for _ in range(self.num_log_lines):
            self.logs.append(fake.sentence())
        with open(log_path, 'w') as file:
            for line in self.logs:
                file.write(line)
                file.write('\n')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = [i for i in resp._iterator]  # pylint:disable=protected-access
        data = [d for d in data[0].decode('utf-8').split('\n') if d]
        assert len(data) == len(self.logs)
        assert data == self.logs
