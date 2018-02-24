# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import exceptions as django_exceptions

from rest_framework import exceptions as rest_exceptions

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser


class ListCreateAPIView(generics.ListCreateAPIView):
    create_serializer_class = None

    def get_serializer_class(self):
        if self.create_serializer_class and self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.serializer_class


class ProtectedView(APIView):
    """Base view for to redirect to a file/path by instructing Nginx
    to do so via special HTTP response headers.
    """
    permission_classes = (IsAuthenticated,)

    NGINX_REDIRECT_HEADER = 'X-Accel-Redirect'

    def handle_exception(self, exc):
        """Use custom exception handler for errors."""
        if isinstance(exc, (rest_exceptions.NotAuthenticated,
                            rest_exceptions.AuthenticationFailed)):
            return HttpResponseRedirect('/app/auth/login?next={}'.format(
                self.request.get_full_path()))

        if isinstance(exc, Http404):
            raise Http404

        if isinstance(exc, rest_exceptions.PermissionDenied):
            raise django_exceptions.PermissionDenied

        return super(ProtectedView, self).handle_exception(exc)

    @classmethod
    def _redirect(cls, path, filename=None):
        response = HttpResponse()
        response['Content-Type'] = u''
        response[cls.NGINX_REDIRECT_HEADER] = path.encode('utf-8')
        if filename:
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response

    def redirect(self, path, filename=None):

        if settings.DEBUG:  # pragma: no cover
            # Redirect to the checked-in test data. Works only with development settings.
            return HttpResponseRedirect(path)

        return self._redirect(path, filename)


class UploadView(APIView):
    """Base view to handle data upload."""
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _handle_posted_data(request, filename, directory, upload_filename):
        file_path = os.path.join(directory, filename)
        file_data = request.data[upload_filename]

        # filename might already exist, if uploads are done in quick succession
        # we just delete the previous one and assume that its changes are already committed
        while os.path.exists(file_path):
            os.remove(file_path)

        # Creating the new file
        with open(file_path, 'wb') as destination:
            for chunk in file_data.chunks():
                destination.write(chunk)
        return file_path
