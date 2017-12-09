# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from functools import wraps

from rest_framework.authentication import TokenAuthentication

from sanic.response import json


class SanicTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.args.get(self.keyword) or request.args.get(self.keyword.lower())

        if not token:
            return None

        return self.authenticate_credentials(token)


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            authorization = SanicTokenAuthentication().authenticate(request)

            if authorization is not None:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)

        return decorated_function

    return decorator
