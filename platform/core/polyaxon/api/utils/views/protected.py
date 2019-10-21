from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.core import exceptions as django_exceptions
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse

import conf

from options.registry.core import DEBUG


class ProtectedView(APIView):
    """Base view for to redirect to a file/path by instructing Nginx
    to do so via special HTTP response headers.
    """
    permission_classes = (IsAuthenticated,)

    NGINX_REDIRECT_HEADER = 'X-Accel-Redirect'
    HANDLE_UNAUTHENTICATED = True

    def handle_exception(self, exc):
        """Use custom exception handler for errors."""
        if isinstance(
            exc, (rest_exceptions.NotAuthenticated,
                  rest_exceptions.AuthenticationFailed)) and self.HANDLE_UNAUTHENTICATED:
            return HttpResponseRedirect('{}?next={}'.format(
                reverse('users:login'),
                self.request.get_full_path()))

        if isinstance(exc, Http404):
            raise Http404()

        if isinstance(exc, rest_exceptions.PermissionDenied):
            raise django_exceptions.PermissionDenied()

        return super().handle_exception(exc)

    @classmethod
    def _redirect(cls, path, filename=None):
        response = HttpResponse()
        response['Content-Type'] = ''
        response[cls.NGINX_REDIRECT_HEADER] = path
        if filename:
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response

    def redirect(self, path, filename=None):

        if conf.get(DEBUG):  # pragma: no cover
            # Redirect to the checked-in test data. Works only with development settings.
            return HttpResponseRedirect(path)

        return self._redirect(path, filename)
