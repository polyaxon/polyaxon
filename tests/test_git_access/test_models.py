import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.git_access import GitAccess
from db.models.owner import Owner
from db.models.secrets import K8SSecret
from factories.factory_git_access import GitAccessFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.git_access_mark
class TestGitAccessModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_has_owner(self):
        git_access = GitAccessFactory()
        self.assertEqual(git_access.has_owner, True)

    def test_create_key_validation_raises_for_same_name(self):
        assert GitAccess.objects.count() == 0
        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='secret1',
                                          secret_ref='secret1')
        GitAccess.objects.create(owner=self.owner,
                                 name='my_github_access',
                                 k8s_secret=secret)
        with self.assertRaises(IntegrityError):
            GitAccess.objects.create(owner=self.owner,
                                     name='my_github_access',
                                     host='https://github.com')

    def test_create_key_validation_passes_for_different_owner(self):
        assert GitAccess.objects.count() == 0
        GitAccess.objects.create(owner=self.owner, name='my_gitlab_access')
        assert GitAccess.objects.count() == 1
        # Using new owner with same keys should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        GitAccess.objects.create(owner=owner, name='my_gitlab_access')
        assert GitAccess.objects.count() == 2

    def test_different_name_and_secret(self):
        registry = GitAccess.objects.create(owner=self.owner,
                                            name='my_gitlab_access',
                                            host='https://gitlab.com')
        assert registry.owner == self.owner
        assert registry.name == 'my_gitlab_access'
        assert registry.k8s_secret is None
        assert registry.db_secret is None
        assert registry.host == 'https://gitlab.com'

        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='secret1',
                                          secret_ref='secret1')
        registry = GitAccess.objects.create(owner=self.owner,
                                            name='my_other_gitlab_access',
                                            k8s_secret=secret,
                                            host='localhost:5000')
        assert registry.owner == self.owner
        assert registry.name == 'my_other_gitlab_access'
        assert registry.k8s_secret == secret
        assert registry.db_secret is None
        assert registry.host == 'localhost:5000'
