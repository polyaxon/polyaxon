# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import requests

from polyaxon_schemas.user import UserConfig

from polyaxon_client.base import PolyaxonClient
from polyaxon_client.exceptions import AuthenticationError


class AuthClient(PolyaxonClient):
    """Auth/User specific client"""
    ENDPOINT = "/user"

    def get_user(self):
        request_url = self._get_url()
        # This is a special case client,
        # because auth_token is not set yet (this is how we verify it)
        # So do not use the shared base client for this!
        response = self.get(request_url,
                            headers={"Authorization": "{} {}".format(
                                self.authentication_type, self.token)})
        try:
            user_dict = response.json()
            response.raise_for_status()
        except Exception:
            if response.status_code == 401:
                raise AuthenticationError(
                    request_url,
                    response,
                    "Invalid Token.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                    401)
            raise AuthenticationError(
                request_url,
                response,
                "Login failed.\nSee http://docs.polyaxon.com/faqs/authentication/ for help",
                response.status_code)

        return UserConfig.from_dict(user_dict)
