from faker import Faker

from rest_framework.response import Response
from rest_framework.views import APIView

from django.test import RequestFactory, TestCase

from api.utils.gzip import gzip


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

    def test_content_encoding_is_set_correctly(self):
        response = self.view(self.factory.get(''))
        assert 'Content-Encoding' in response
        assert response['Content-Encoding'] == 'gzip'

    def test_content_encoding_is_set_correctly_after_subclassing(self):
        response = self.subclass_view(self.factory.get(''))
        assert 'Content-Encoding' not in response
