# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

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


class DownloadView(APIView):
    """Base view for to redirect to a file by instructing Nginx
    to do so via special HTTP response headers.
    """
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def _redirect_to_file(path):
        response = HttpResponse()
        response['Content-Type'] = u''
        response['X-Accel-Redirect'] = path.encode('utf-8')

        return response

    def get(self, request, file_path):

        if settings.DEBUG:  # pragma: no cover
            # Redirect to the checked-in test data. Works only with development settings.
            return HttpResponseRedirect(file_path)

        return self._redirect_to_file(file_path)


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
