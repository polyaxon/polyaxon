#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework.mixins import CreateModelMixin as DJRCreateModelMixin
from rest_framework.mixins import DestroyModelMixin as DJRDestroyModelMixin
from rest_framework.mixins import ListModelMixin as DRFListModelMixin
from rest_framework.mixins import RetrieveModelMixin as DRFRetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin as DJRUpdateModelMixin


class CreateModelMixin(DJRCreateModelMixin):
    """
    Create a model instance.
    """


class ListModelMixin(DRFListModelMixin):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.audit(request, *args, **kwargs)
        return response


class RetrieveModelMixin(DRFRetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        self.audit(request, *args, **kwargs)
        return response


class UpdateModelMixin(DJRUpdateModelMixin):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.audit(request, *args, **kwargs)
        return response


class DestroyModelMixin(DJRDestroyModelMixin):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.audit(request, *args, **kwargs)
        return response
