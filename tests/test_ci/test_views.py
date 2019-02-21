import pytest

from rest_framework import status

from api.ci.serializers import CISerializer
from constants.urls import API_V1
from db.models.ci import CI
from factories.ci_factory import CIFactory
from factories.factory_projects import ProjectFactory
from tests.utils import BaseViewTest


@pytest.mark.ci_mark
class TestCIViewV1(BaseViewTest):
    serializer_class = CISerializer
    model_class = CI
    factory_class = CIFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.project2 = ProjectFactory(user=self.auth_client.user)
        self.object = self.factory_class(project=self.project, user=self.auth_client.user)
        self.unauthorised_object = self.factory_class()
        self.url = '/{}/{}/{}/ci'.format(API_V1,
                                         self.project.user.username,
                                         self.project.name)
        self.url2 = '/{}/{}/{}/ci'.format(API_V1,
                                          self.project2.user.username,
                                          self.project2.name)
        self.unauthorised_url = '/{}/{}/{}/ci'.format(
            API_V1,
            self.unauthorised_object.project.user.username,
            self.unauthorised_object.project.name)

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.object).data

        # unauthorised object get works
        resp = self.auth_client.get(self.unauthorised_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(self.unauthorised_object).data

    def test_patch(self):
        data = {'config': {'foo': 'bar'}}
        resp = self.auth_client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK
        new_object = self.model_class.objects.get(id=self.object.id)
        assert new_object.project == self.object.project
        assert new_object.config == data['config']

    def test_delete(self):
        assert self.model_class.objects.count() == 2
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.count() == 1

        # unauthorised object delete not working
        resp = self.auth_client.delete(self.unauthorised_url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        assert self.model_class.objects.count() == 2
        resp = self.auth_client.post(self.url2)
        assert resp.status_code == 201
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == 3
