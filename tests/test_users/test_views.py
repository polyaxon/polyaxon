from rest_framework import status
from tests.utils import BaseViewTest

from django.contrib.auth import get_user_model

from factories.factory_users import UserFactory
from polyaxon.urls import API_V1


class TestActivateViewV1(BaseViewTest):
    model_class = get_user_model()
    factory_class = UserFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.admin = self.factory_class(is_staff=True, is_superuser=True)
        self.user = self.factory_class(is_staff=False, is_superuser=False)
        self.inactive_user = self.factory_class(is_staff=False, is_superuser=False, is_active=False)
        self.url = '/{}/users/activate/{}'.format(API_V1,
                                                  self.inactive_user.username)

    def test_activate_works_as_expected(self):
        # normal user
        self.auth_client.login_user(self.user)
        resp = self.auth_client.post(self.url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        user = self.model_class.objects.get(pk=self.inactive_user.pk)
        assert user.is_active is False

        # admin user
        self.auth_client.login_user(self.admin)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        user = self.model_class.objects.get(pk=self.inactive_user.pk)
        assert user.is_active is True


class TestDeleteViewV1(BaseViewTest):
    model_class = get_user_model()
    factory_class = UserFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.admin = self.factory_class(is_staff=True, is_superuser=True)
        self.user = self.factory_class(is_staff=False, is_superuser=False)
        self.other_user = self.factory_class()
        self.url = '/{}/users/delete/{}'.format(API_V1,
                                                self.other_user.username)

    def test_delete_works_as_expected(self):
        # normal user
        self.auth_client.login_user(self.user)
        resp = self.auth_client.delete(self.url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        assert self.model_class.objects.filter(pk=self.other_user.pk).count() == 1

        # admin user
        self.auth_client.login_user(self.admin)
        resp = self.auth_client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.model_class.objects.filter(pk=self.other_user.pk).count() == 0


class TestGrantSuperuserViewV1(BaseViewTest):
    model_class = get_user_model()
    factory_class = UserFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.admin = self.factory_class(is_staff=True, is_superuser=True)
        self.user = self.factory_class(is_staff=False, is_superuser=False)
        self.normal_user = self.factory_class(is_staff=False, is_superuser=False)
        self.url = '/{}/superusers/grant/{}'.format(API_V1,
                                                    self.normal_user.username)

    def test_grant_works_as_expected(self):
        # normal user
        self.auth_client.login_user(self.user)
        resp = self.auth_client.post(self.url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        user = self.model_class.objects.get(pk=self.normal_user.pk)
        assert user.is_staff is False
        assert user.is_superuser is False

        # admin user
        self.auth_client.login_user(self.admin)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        user = self.model_class.objects.get(pk=self.normal_user.pk)
        assert user.is_staff is True
        assert user.is_superuser is True


class TestRevokeSuperuserViewV1(BaseViewTest):
    model_class = get_user_model()
    factory_class = UserFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.auth_user = self.auth_client.user
        self.admin = self.factory_class(is_staff=True, is_superuser=True)
        self.user = self.factory_class(is_staff=False, is_superuser=False)
        self.other_admin_user = self.factory_class(is_staff=True, is_superuser=True)
        self.url = '/{}/superusers/revoke/{}'.format(API_V1,
                                                     self.other_admin_user.username)

    def test_revoke_works_as_expected(self):
        # normal user
        self.auth_client.login_user(self.user)
        resp = self.auth_client.post(self.url)
        assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
        user = self.model_class.objects.get(pk=self.other_admin_user.pk)
        assert user.is_staff is True
        assert user.is_superuser is True

        # admin user
        self.auth_client.login_user(self.admin)
        resp = self.auth_client.post(self.url)
        assert resp.status_code == status.HTTP_200_OK
        user = self.model_class.objects.get(pk=self.other_admin_user.pk)
        assert user.is_staff is False
        assert user.is_superuser is False
