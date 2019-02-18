import pytest

from hestia.internal_services import InternalServices
from rest_framework import status

from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from constants.urls import API_V1
from factories.factory_experiments import ExperimentFactory
from factories.factory_jobs import JobFactory
from factories.factory_plugins import NotebookJobFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest, InternalClient


@pytest.mark.impersonatetokens_mark
class TestBaseImpersonateTokenViewV1(BaseViewTest):
    HAS_AUTH = False
    HAS_INTERNAL = True
    INTERNAL_SERVICE = InternalServices.INITIALIZER
    LIFE_CYCLE = None
    factory_class = None

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.project = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=self.project,  # pylint:disable=not-callable
                                         user=self.auth_client.user)
        self.url = self.get_url()

    def get_url(self):
        return ''

    def test_is_forbidden_for_other_clients(self):
        statuses = {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN}
        resp = self.client.post(self.url)
        assert resp.status_code in statuses
        resp = self.auth_client.post(self.url)
        assert resp.status_code in statuses
        internal = InternalClient(service=InternalServices.DOCKERIZER)
        resp = internal.post(self.url)
        assert resp.status_code in statuses

    def test_is_forbidden_for_non_running_or_scheduled_object(self):
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_using_scheduled_object_token(self):
        self.object.set_status(status=self.LIFE_CYCLE.SCHEDULED)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.object.user.tokens.last().key}

    def test_using_running_object_token(self):
        self.object.set_status(status=self.LIFE_CYCLE.RUNNING)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.object.user.tokens.last().key}


@pytest.mark.impersonatetokens_mark
class TestExperimentImpersonateTokenViewV1(TestBaseImpersonateTokenViewV1):
    factory_class = ExperimentFactory
    LIFE_CYCLE = ExperimentLifeCycle

    def get_url(self):
        return '/{}/{}/{}/experiments/{}/imporsonatetoken'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)

    def test_using_starting_object_token(self):
        self.object.set_status(status=ExperimentLifeCycle.STARTING)
        resp = self.internal_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == {'token': self.object.user.tokens.last().key}


@pytest.mark.impersonatetokens_mark
class TestJobImpersonateTokenViewV1(TestBaseImpersonateTokenViewV1):
    factory_class = JobFactory
    LIFE_CYCLE = JobLifeCycle

    def get_url(self):
        return '/{}/{}/{}/jobs/{}/imporsonatetoken'.format(
            API_V1,
            self.project.user.username,
            self.project.name,
            self.object.id)


@pytest.mark.impersonatetokens_mark
class TestNotebookImpersonateTokenViewV1(TestBaseImpersonateTokenViewV1):
    factory_class = NotebookJobFactory
    LIFE_CYCLE = JobLifeCycle

    def get_url(self):
        return '/{}/{}/{}/notebook/imporsonatetoken'.format(
            API_V1,
            self.project.user.username,
            self.project.name)


del TestBaseImpersonateTokenViewV1
