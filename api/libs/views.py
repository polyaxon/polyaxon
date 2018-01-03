# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from rest_framework import generics


class ListCreateAPIView(generics.ListCreateAPIView):
    create_serializer_class = None

    def get_serializer_class(self):
        if self.create_serializer_class and self.request.method.lower() == 'post':
            return self.create_serializer_class
        return self.serializer_class
