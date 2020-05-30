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

from faker import Faker

from django.test import RequestFactory, TestCase
from flaky import flaky
from rest_framework.response import Response
from rest_framework.views import APIView

from polycommon.apis.gzip import gzip


class TestGZip(TestCase):
    def setUp(self):
        super(TestGZip, self).setUp()
        fake = Faker()

        class TestView(APIView):
            @gzip()
            def get(self, request, *args, **kwargs):
                """Example to check `Content-Encoding` header is set to 'gzip'."""
                return Response(status=200, data=fake.text())

        class SubClassTestView(TestView):
            def get(self, request, *args, **kwargs):
                """Example to check that no status is set after overriding inherited endpoints."""
                return Response(status=200, data=fake.text())

        self.view = TestView.as_view()
        self.subclass_view = SubClassTestView.as_view()
        self.factory = RequestFactory()

    @flaky(max_runs=3)
    def test_content_encoding_is_set_correctly(self):
        response = self.view(self.factory.get(""))
        assert "Content-Encoding" in response
        assert response["Content-Encoding"] == "gzip"

    @flaky(max_runs=3)
    def test_content_encoding_is_set_correctly_after_subclassing(self):
        response = self.subclass_view(self.factory.get(""))
        assert "Content-Encoding" not in response
