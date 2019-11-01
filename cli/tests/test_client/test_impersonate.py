# coding: utf-8
from __future__ import absolute_import, division, print_function

import os
import tempfile
import uuid

from unittest import TestCase

from mock import patch

from polyaxon.client.utils import create_context_auth, impersonate
from polyaxon.schemas.api.authentication import AccessTokenConfig


class TestImpersonate(TestCase):
    def test_create_context_auth(self):
        token = uuid.uuid4().hex
        context_mount = tempfile.mkdtemp()
        context_mount_auth = "{}/.polyaxonauth".format(context_mount)

        # Login without updating the token and without persistence
        if os.path.exists(context_mount_auth):
            os.remove(context_mount_auth)

        assert os.path.exists(context_mount_auth) is False
        create_context_auth(AccessTokenConfig(token=token), context_mount_auth)
        assert os.path.exists(context_mount_auth) is True

    @patch("polyaxon_sdk.RunsV1Api.impersonate_token")
    @patch("polyaxon.client.utils.create_context_auth")
    def test_login_impersonate(self, create_context, impersonate_token):

        impersonate(owner="owner", project="project", run_uuid=uuid.uuid4().hex)
        assert impersonate_token.call_count == 1
        assert create_context.call_count == 1
