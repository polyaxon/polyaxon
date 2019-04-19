import os
import tempfile

from rest_framework import status

from api.code_reference.serializers import CodeReferenceSerializer
from db.models.repos import CodeReference
from factories.factory_code_reference import CodeReferenceFactory
from factories.factory_projects import ProjectFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest
from tests.base.clients import AuthorizedClient, InternalClient


class BaseViewTest(BaseTest):
    """This is the base test for all tests.

    Also mocks common external calls, e.g. for tracking or related to auth.
    """

    HAS_AUTH = False
    HAS_INTERNAL = False
    ADMIN_USER = False
    INTERNAL_SERVICE = None

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.internal_client = InternalClient(service=cls.INTERNAL_SERVICE)
        if cls.ADMIN_USER:
            user = UserFactory(is_staff=True, is_superuser=True)
            cls.auth_client = AuthorizedClient(user=user)
        else:
            cls.auth_client = AuthorizedClient()

    def setUp(self):
        assert hasattr(self, 'auth_client') and self.auth_client is not None
        super().setUp()

    def test_requires_auth(self):
        # Test unauthorized access to view
        if self.HAS_AUTH:
            assert hasattr(self, 'url'), 'Cannot check auth if url is not set.'
            assert self.client.get(self.url).status_code in (status.HTTP_401_UNAUTHORIZED,
                                                             status.HTTP_403_FORBIDDEN)
            if not self.HAS_INTERNAL:
                assert self.internal_client.get(self.url).status_code in (
                    status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


class BaseFilesViewTest(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.url_second_level = ''
        self.url_second_level2 = ''
        self.top_level = {}
        self.top_level_files = []
        self.second_level = {}
        self.second_level_files = []

    def create_paths(self, path, url):
        # Create files
        fpath1 = path + '/test1.txt'
        with open(fpath1, 'w') as f:
            f.write('data1')
        fsize1 = os.path.getsize(fpath1)
        fpath2 = path + '/test2.txt'
        with open(fpath2, 'w') as f:
            f.write('data2')
        fsize2 = os.path.getsize(fpath2)
        # Create dirs
        dirname1 = tempfile.mkdtemp(prefix=path + '/')
        dirname2 = tempfile.mkdtemp(prefix=path + '/')
        self.top_level_files = [
            {'file': 'test1.txt', 'data': 'data1'},
            {'file': 'test2.txt', 'data': 'data2'}]
        self.top_level = {'files': [('test1.txt', fsize1), ('test2.txt', fsize2)],
                          'dirs': [dirname1.split('/')[-1], dirname2.split('/')[-1]]}

        # Create dirs under dirs
        self.url_second_level = url + '?path={}'.format(dirname1.split('/')[-1])
        self.url_second_level2 = url + '?path={}'.format(dirname1.split('/')[-1] + '/')
        dirname3 = tempfile.mkdtemp(prefix=dirname1 + '/')
        # Create files under dirs
        fpath1 = dirname1 + '/test11.txt'
        with open(fpath1, 'w') as f:
            f.write('data11')
        fsize1 = os.path.getsize(fpath1)

        fpath2 = dirname1 + '/test12.txt'
        with open(fpath2, 'w') as f:
            f.write('data12')
        fsize2 = os.path.getsize(fpath2)
        self.second_level_files = [
            {'file': dirname1.split('/')[-1] + '/test11.txt', 'data': 'data11'},
            {'file': dirname1.split('/')[-1] + '/test12.txt', 'data': 'data12'}]
        self.second_level = {'files': [('test11.txt', fsize1), ('test12.txt', fsize2)],
                             'dirs': [dirname3.split('/')[-1]]}

    def assert_same_content(self, value1, value2):
        assert len(value1) == len(value2)
        assert set(value1) == set(value2)


class EntityCodeReferenceBaseViewTest(BaseViewTest):
    serializer_class = CodeReferenceSerializer
    model_class = CodeReference
    factory_class = CodeReferenceFactory
    entity_factory_class = None

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory(user=self.auth_client.user)
        self.obj = self.entity_factory_class(project=self.project)
        self.url = self.get_url()
        self.queryset = self.model_class.objects.all()

    def get_url(self):
        raise NotImplementedError()

    def test_get(self):
        coderef = CodeReferenceFactory()
        self.obj.code_reference = coderef
        self.obj.save()
        resp = self.auth_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data == self.serializer_class(coderef).data

    def test_create(self):
        count = self.model_class.objects.count()
        data = {}
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == count + 1
        last_object = self.model_class.objects.last()
        self.obj.refresh_from_db()
        assert last_object == self.obj.code_reference
        assert last_object.branch == 'master'
        assert last_object.commit is None
        assert last_object.head is None
        assert last_object.is_dirty is False
        assert last_object.git_url is None
        assert last_object.repo is None
        assert last_object.external_repo is None

        data = {
            'commit': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'head': '3783ab36703b14b91b15736fe4302bfb8d52af1c',
            'branch': 'feature1',
            'git_url': 'https://bitbucket.org:foo/bar.git',
            'is_dirty': True
        }
        resp = self.auth_client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == count + 2
        last_object = self.model_class.objects.last()
        self.obj.refresh_from_db()
        assert last_object == self.obj.code_reference
        assert last_object.branch == 'feature1'
        assert last_object.commit == '3783ab36703b14b91b15736fe4302bfb8d52af1c'
        assert last_object.head == '3783ab36703b14b91b15736fe4302bfb8d52af1c'
        assert last_object.is_dirty is True
        assert last_object.git_url == 'https://bitbucket.org:foo/bar.git'
        assert last_object.repo is None
        assert last_object.external_repo is None
