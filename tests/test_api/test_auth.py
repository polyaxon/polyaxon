# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import httpretty
import json
import os
import tempfile
import uuid

from tests.test_api.utils import TestBaseApi

from polyaxon_client import settings
from polyaxon_client.api.auth import AuthApi
from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.schemas import CredentialsConfig, UserConfig


class TestAuthApi(TestBaseApi):

    def setUp(self):
        super(TestAuthApi, self).setUp()
        settings.CONTEXT_AUTH_TOKEN_PATH = '{}/{}'.format(tempfile.mkdtemp(), '.authtoken')
        settings.TMP_AUTH_TOKEN_PATH = '{}/{}'.format(tempfile.mkdtemp(), '.authtoken')
        self.api_handler = AuthApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_user(self):
        user = UserConfig('user', 'user@test.com').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/users'),
            body=json.dumps(user),
            content_type='application/json', status=200)

        # Schema response
        result = self.api_handler.get_user('token_value')
        assert result.to_dict() == user

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_user('token_value')
        assert result == user

    @httpretty.activate
    def test_login(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/users',
                'token'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        # Login without updating the token
        assert self.api_config.token == 'token'
        credentials = CredentialsConfig('user', 'password')
        assert token == self.api_handler.login(credentials=credentials, set_token=False)
        assert self.api_config.token == 'token'

        # Login and update the token
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login(credentials=credentials, set_token=True)
        assert self.api_config.token == token

    @httpretty.activate
    def test_login_experiment_ephemeral_token(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments',
                '1',
                'ephemeraltoken'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        # Login without updating the token and without persistence
        if os.path.exists(settings.TMP_AUTH_TOKEN_PATH):
            os.remove(settings.TMP_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_experiment_ephemeral_token(
            username='user',
            project_name='project',
            experiment_id=1,
            ephemeral_token='foo',
            set_token=False,
            persist_token=False)
        assert self.api_config.token == 'token'
        assert os.path.exists(settings.TMP_AUTH_TOKEN_PATH) is False

        # Login and update the token and persistence
        if os.path.exists(settings.TMP_AUTH_TOKEN_PATH):
            os.remove(settings.TMP_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_experiment_ephemeral_token(
            username='user',
            project_name='project',
            experiment_id=1,
            ephemeral_token='foo',
            set_token=True,
            persist_token=True)
        assert self.api_config.token == token
        assert os.path.exists(settings.TMP_AUTH_TOKEN_PATH) is True

        # Login remove ephemeral token from env var and settings
        os.environ[settings.SECRET_EPHEMERAL_TOKEN_KEY] = 'value'
        settings.SECRET_EPHEMERAL_TOKEN = 'eph_token'  # noqa
        if os.path.exists(settings.TMP_AUTH_TOKEN_PATH):
            os.remove(settings.TMP_AUTH_TOKEN_PATH)
        assert self.api_config.token == token
        assert os.environ.get(settings.SECRET_EPHEMERAL_TOKEN_KEY) == 'value'
        assert settings.SECRET_EPHEMERAL_TOKEN == 'eph_token'
        assert token == self.api_handler.login_experiment_ephemeral_token(
            username='user',
            project_name='project',
            experiment_id=1,
            ephemeral_token='foo',
            set_token=True,
            persist_token=True)
        assert self.api_config.token == token
        assert os.path.exists(settings.TMP_AUTH_TOKEN_PATH) is True
        assert os.environ.get(settings.SECRET_EPHEMERAL_TOKEN_KEY) is None
        assert not hasattr(settings, 'SECRET_EPHEMERAL_TOKEN')

        assert token == self.api_handler.login_experiment_ephemeral_token(
            username='user',
            project_name='project',
            experiment_id=1,
            ephemeral_token='foo',
            set_token=True,
            persist_token=True)

    @httpretty.activate
    def test_login_experiment_impersonate_token(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'experiments',
                '1',
                'imporsonatetoken'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        # Login without updating the token and without persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_experiment_impersonate_token(
            username='user',
            project_name='project',
            experiment_id=1,
            internal_token='foo',
            set_token=False,
            persist_token=False)
        assert self.api_config.token == 'token'
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is False

        # Login and update the token and persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_experiment_impersonate_token(
            username='user',
            project_name='project',
            experiment_id=1,
            internal_token='foo',
            set_token=True,
            persist_token=True)
        assert self.api_config.token == token
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is True

    @httpretty.activate
    def test_login_job_impersonate_token(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'jobs',
                '1',
                'imporsonatetoken'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        # Login without updating the token and without persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_job_impersonate_token(
            username='user',
            project_name='project',
            job_id=1,
            internal_token='foo',
            set_token=False,
            persist_token=False)
        assert self.api_config.token == 'token'
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is False

        # Login and update the token and persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_job_impersonate_token(
            username='user',
            project_name='project',
            job_id=1,
            internal_token='foo',
            set_token=True,
            persist_token=True)
        assert self.api_config.token == token
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is True

    @httpretty.activate
    def test_login_notebook_impersonate_token(self):
        token = uuid.uuid4().hex
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'user',
                'project',
                'notebook',
                'imporsonatetoken'
            ),
            body=json.dumps({'token': token}),
            content_type='application/json', status=200)

        # Login without updating the token and without persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_notebook_impersonate_token(
            username='user',
            project_name='project',
            internal_token='foo',
            set_token=False,
            persist_token=False)
        assert self.api_config.token == 'token'
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is False

        # Login and update the token and persistence
        if os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH):
            os.remove(settings.CONTEXT_AUTH_TOKEN_PATH)
        assert self.api_config.token == 'token'
        assert token == self.api_handler.login_notebook_impersonate_token(
            username='user',
            project_name='project',
            internal_token='foo',
            set_token=True,
            persist_token=True)
        assert self.api_config.token == token
        assert os.path.exists(settings.CONTEXT_AUTH_TOKEN_PATH) is True
