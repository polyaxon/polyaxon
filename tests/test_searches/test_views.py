import pytest

from rest_framework import status

from api.searches.serializers import SearchSerializer
from constants import content_types
from constants.urls import API_V1
from db.models.searches import Search
from factories.factory_projects import ProjectFactory
from factories.factory_searches import SearchFactory
from tests.utils import BaseViewTest


@pytest.mark.search_mark
class BaseTestSearchListView(BaseViewTest):
    HAS_AUTH = True
    model_class = Search
    factory_class = SearchFactory
    serializer_class = SearchSerializer
    entity = ''
    content_type = ''
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.other_project = ProjectFactory()
        self.url = '/{}/searches/{}/{}/{}'.format(API_V1,
                                                  self.project.user.username,
                                                  self.project.name,
                                                  self.entity)
        self.other_url = '/{}/searches/{}/{}/{}'.format(API_V1,
                                                        self.other_project.user.username,
                                                        self.other_project.name,
                                                        self.entity)
        self.objects = [
            self.factory_class(user=self.auth_client.user,
                               project=self.project,
                               content_type=self.content_type) for _ in range(self.num_objects)]

        # Other objects that do not belong to the filter
        self.factory_class(project=self.other_project, content_type=self.content_type)
        self.queryset = self.model_class.objects.filter(project=self.project)
        self.queryset = self.queryset.order_by('-updated_at')

    def test_get(self):
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data['next'] is None
        assert resp.data['count'] == len(self.objects)

        data = resp.data['results']
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        resp = self.auth_client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['count'] == 0

    def test_create(self):
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {'query': {'query': 'project.id: 1|2', 'sort': '-created_at'}}
        resp = self.auth_client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert self.queryset.count() == self.num_objects + 1

        # Test other
        resp = self.auth_client.post(self.other_url, data)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.search_mark
class BaseTestSearchDeleteView(BaseViewTest):
    DISABLE_RUNNER = True
    DISABLE_EXECUTOR = True
    HAS_AUTH = True
    model_class = Search
    factory_class = SearchFactory
    serializer_class = SearchSerializer
    entity = ''
    content_type = ''

    def get_url(self, obj):
        return '/{}/searches/{}/{}/{}/{}'.format(API_V1,
                                                 self.project.user.username,
                                                 self.project.name,
                                                 self.entity,
                                                 obj.id)

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        some_object = self.factory_class(project=self.project,
                                         content_type=self.content_type)
        self.url = self.get_url(some_object)

    def test_delete(self):
        assert Search.objects.count() == 1
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        obj = self.factory_class(user=self.auth_client.user,
                                 project=self.project,
                                 content_type=self.content_type)
        assert Search.objects.count() == 2
        resp = self.auth_client.delete(self.get_url(obj))
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert Search.objects.count() == 1


@pytest.mark.search_mark
class TestExperimentSearchCreateView(BaseTestSearchListView):
    entity = 'experiments'
    content_type = content_types.EXPERIMENT


@pytest.mark.search_mark
class TestExperimentSearchDeleteView(BaseTestSearchDeleteView):
    entity = 'experiments'
    content_type = content_types.EXPERIMENT


@pytest.mark.search_mark
class TestExperimentGroupSearchCreateView(BaseTestSearchListView):
    entity = 'groups'
    content_type = content_types.EXPERIMENT_GROUP


@pytest.mark.search_mark
class TestExperimentGroupSearchDeleteView(BaseTestSearchDeleteView):
    entity = 'groups'
    content_type = content_types.EXPERIMENT_GROUP


@pytest.mark.search_mark
class TestJobSearchCreateView(BaseTestSearchListView):
    entity = 'jobs'
    content_type = content_types.JOB


@pytest.mark.search_mark
class TestJobSearchDeleteView(BaseTestSearchDeleteView):
    entity = 'jobs'
    content_type = content_types.JOB


@pytest.mark.search_mark
class TestBuildSearchCreateView(BaseTestSearchListView):
    entity = 'builds'
    content_type = content_types.BUILD_JOB


@pytest.mark.search_mark
class TestBuildSearchDeleteView(BaseTestSearchDeleteView):
    entity = 'builds'
    content_type = content_types.BUILD_JOB


del BaseTestSearchListView
del BaseTestSearchDeleteView
