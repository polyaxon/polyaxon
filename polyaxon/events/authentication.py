from functools import wraps

from rest_framework.authentication import TokenAuthentication

from sanic.response import json


class SanicTokenAuthentication(TokenAuthentication):
    AUTHORIZATION_HEADER = 'Authorization'

    def authenticate(self, request):
        # Check headers
        token = request.headers.get(self.AUTHORIZATION_HEADER) or request.headers.get(self.AUTHORIZATION_HEADER.lower())
        if token:
            token = token.split(' ')
            if len(token) == 2 and (token[0] == self.keyword or token[0] == self.keyword.lower()):
                token = token[1]
            else:
                token = None

        # Check args
        if not token:
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
                request.app.user = authorization[0]
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)

        return decorated_function

    return decorator
